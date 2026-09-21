import os
import pprint
import pwd
import time
import shutil
import logging
import tempfile
import subprocess

from celery import shared_task
from django.conf import settings
from django.utils import timezone
from django.core.files import File
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django_auth_ldap.backend import LDAPBackend

from celery_app.app import app
from core.services.redis_service import sync_redis_client
from core.models import ArgType, ProcessingModel, ProcessingStatus
from core.services.monitor_logger import transform_redis_logs_stream_to_str, get_type_line


logger = logging.getLogger(__name__)


def _send_file_download_status(input_file):
    """Отправить обновление статуса загрузки файла пользователю через WebSocket."""
    if not getattr(input_file, 'user_id', None):
        return
    channel_layer = get_channel_layer()
    logger.info(f"STATUS: {input_file.download_status}, {input_file.get_download_status_display()}")
    async_to_sync(channel_layer.group_send)(
        f'files_user_{input_file.user_id}',
        {
            'type': 'send_file_download_status',
            'file_id': str(input_file.id),
            'status': input_file.download_status,
            'status_display': input_file.get_download_status_display(),
            'file_size_mb': input_file.get_file_size_mb(),
            'is_remote': input_file.is_remote,
            'error': input_file.download_error or '',
        }
    )


def _mark_file_download_failed(input_file, error: str):
    """Отметить файл как нескачанный и уведомить через WebSocket."""
    from core.models import DownloadStatus

    input_file.download_status = DownloadStatus.FAILED
    input_file.download_error = error
    input_file.save(update_fields=['download_status', 'download_error'])
    _send_file_download_status(input_file)


@app.task()
def download_file_task(file_id: str):
    """
    Celery задача скачивания удалённого файла (HTTP/FTP) в MEDIA_ROOT.

    Args:
        file_id: UUID записи InputFile
    """

    from core.models import InputFileModel, DownloadStatus
    from core.services import downloader

    try:
        input_file = InputFileModel.objects.select_related('user').get(id=file_id)
    except InputFileModel.DoesNotExist:
        logger.error(f"download_file_task: файл {file_id} не найден")
        return

    # Переход в статус «Скачивается»
    input_file.download_status = DownloadStatus.DOWNLOADING
    input_file.download_error = ''
    input_file.save(update_fields=['download_status', 'download_error'])
    _send_file_download_status(input_file)

    logger.info(f"Updated status file ({input_file.id}) to {DownloadStatus.DOWNLOADING.name}")

    password = downloader.verify_secret(input_file.ftp_password)
    tmp_dir = tempfile.mkdtemp(prefix='algmanager_dl_')
    tmp_path = os.path.join(tmp_dir, 'download.tmp')

    try:
        downloader.download_to_disk(
            input_file.source_url,
            tmp_path,
            username=input_file.ftp_username or '',
            password=password,
        )
        logger.info(f"download_to_disk ({input_file.id})")

        name = downloader.derive_filename(
            input_file.source_url,
            fallback=input_file.name or 'download.h5',
        )
        logger.info(f"derive_filename ({input_file.id}), result = {name}")

        size = os.path.getsize(tmp_path)
        with open(tmp_path, 'rb') as fobj:
            input_file.filename.save(name, File(fobj), save=False)

        logger.info(f"saving file ({input_file.id}), tmp_path = {tmp_path}")

        input_file.original_filename = name
        input_file.file_size = size
        input_file.download_status = DownloadStatus.COMPLETED
        input_file.download_error = ''
        input_file.save()

        logger.info(f"download_file_task: скачан {name} ({size} байт)")

        _send_file_download_status(input_file)

    except downloader.DownloadError as e:
        logger.error(f"download_file_task: {file_id}: {e}")
        _mark_file_download_failed(input_file, str(e))
    except Exception as e:
        logger.exception(f"download_file_task: {file_id}: {e}")
        _mark_file_download_failed(input_file, str(e))
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)


def _send_run_update(run_id: str, status: str, progress: int = None, current_step: str = ''):
    """Отправить обновление статуса через WebSocket."""
    channel_layer = get_channel_layer()

    update_data = {
        'status': status,
    }
    if progress is not None:
        update_data['progress'] = progress
    if current_step:
        update_data['current_step'] = current_step

    async_to_sync(channel_layer.group_send)(
        f'run_{run_id}',
        {'type': 'send_status_update', **update_data}
    )


def _send_log_update(run_id: str, message: str, line: int = 0):
    """Отправить обновление лога через WebSocket."""
    channel_layer = get_channel_layer()
    line_class = get_type_line(message)
    async_to_sync(channel_layer.group_send)(
        f'run_{run_id}',
        {
            'type': 'send_log_update',
            'message': message,
            'class': line_class,
            'line': line
        }
    )


def _get_ldap_user_info(username):
    user = LDAPBackend().populate_user(username)
    if not user:
        raise Exception(f"Пользователь {username} не найден (Был создан через web-сервис)")
    user_info = pwd.getpwnam(user.ldap_username)
    return user_info


def _check_count_running_task(self_task, max_parallel_processes=1):
    from celery_app.app import app

    active_data = app.control.inspect().active()
    if active_data:
        for worker, tasks in active_data.items():
            if worker == self_task.request.hostname:
                current_tasks = list(filter(lambda item: item['type'] == self_task.name, tasks))
                if len(current_tasks) - 1 >= max_parallel_processes:
                    return True

    return False


@shared_task(bind=True, max_retries=None)
def run_algorithm_task(self, run_id: str):
    """
    Celery задача для запуска алгоритма обработки.

    Args:
        run_id: UUID запуска алгоритма
    """

    try:
        # Получение запуска
        processing = ProcessingModel.objects.select_related('algorithm', 'user').get(id=run_id)

        if _check_count_running_task(self, processing.algorithm.max_parallel_processes):
            logger.warning(f"Задача вернулась обратно в очередь {run_id}")
            self.retry(countdown=20, throw=False)
            return

        # Проверка статуса
        if processing.status == ProcessingStatus.CANCELLED:
            logger.info(f"Запуск {run_id} отменён до начала выполнения")
            return

        # Обновление статуса
        processing.status = ProcessingStatus.RUNNING
        processing.started_at = timezone.now()
        processing.save(update_fields=['status', 'started_at'])

        _send_run_update(run_id, ProcessingStatus.RUNNING)
        _send_log_update(run_id, f"Запуск алгоритма {processing.algorithm.name}")

        logger.info(f"Запуск алгоритма {processing.algorithm.name}")

        # Подготовка путей
        script_path = processing.algorithm.script_path

        logger.info(f"Подготовка путей для alg_id:{run_id}")

        logs_dir = os.path.join(settings.MEDIA_ROOT, 'logs', str(processing.id))
        os.makedirs(logs_dir, exist_ok=True)

        logger.info(f"Создание output дирeктории {logs_dir}, alg_id:{run_id}")

        # Формирование аргументов для скрипта
        script_args = []

        # Добавляем дополнительные аргументы (из формы запуска, таблица ProcessingArgOption)
        logger.info("Добавляем дополнительные аргументы (из формы запуска, таблица ProcessingArgOption)")

        extra_display = []
        sudo_display = []
        cmd = []
        for extra in processing.arguments.select_related('input_file').order_by('argument_order'):
            arg = (extra.option or '').strip()
            if not extra.use_sudo:

                if not arg and extra.arg_type != ArgType.FILE:
                    continue

                value = extra.value or ''

                # Разрешение файла, если путь не был зафиксирован в view
                if extra.arg_type == ArgType.FILE_ARG and not value and extra.input_file_id:
                    value = extra.input_file.filename.path

                if value:
                    script_args.extend([arg, value])
                    extra_display.append(f"{arg}={value}")
                else:
                    script_args.append(arg)
                    extra_display.append(arg)

            else:
                if not arg:
                    continue
                if extra.arg_type == ArgType.VALUE and (extra.value or '').strip():
                    value = extra.value.strip()
                    cmd.extend([arg, value])
                    sudo_display.append(f"{arg}={value}")
                else:
                    cmd.append(arg)
                    sudo_display.append(arg)

        if extra_display:
            _send_log_update(run_id, f"Дополнительные аргументы: {', '.join(extra_display)}")
            logger.info(f"Дополнительные аргументы: {', '.join(extra_display)}")

        _send_log_update(run_id, "Запуск с sudo")
        if sudo_display:
            cmd = ['sudo'] + cmd
            _send_log_update(run_id, f"Опции sudo: {', '.join(sudo_display)}")

        # Лог файл
        log_file = os.path.join(logs_dir, 'processing.log')
        processing.log_file = log_file
        logger.info(f"Добавление логфайла - {log_file}")
        processing.save(update_fields=['log_file'])

        _send_log_update(run_id, f"Скрипт: {script_path}")
        _send_log_update(run_id, f"Входной файл: input_file_path")
        # send_log_update(run_id, f"Выходная директория: {output_dir}")

        # Проверка существования скрипта
        logger.info(f"Проверка существования скрипта {script_path}")
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"Скрипт не найден: {script_path}")

        # Запуск скрипта

        user_info = _get_ldap_user_info(processing.user.username)

        cmd.extend(['bash', script_path])
        cmd.extend(script_args)

        logger.info(f"Запуск скрипта {cmd}")
        _send_log_update(run_id, "Начало выполнения...")

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
            user=user_info.pw_uid,
            group=user_info.pw_gid,
        )

        # Чтение вывода в реальном времени
        logger.info("Чтение вывода в реальном времени ->")
        line_num = 0

        for line in iter(process.stdout.readline, ''):
            if line:
                line = line.strip()
                logger.info(f"[Run {run_id}] {line}")

                # Отправка лога через WebSocket
                _send_log_update(run_id, line, line_num)

                fields = {
                    "line": line_num,
                    "class": get_type_line(line),
                    "message": line,
                }
                sync_redis_client.xadd(f"app_logs_stream_{run_id}", fields=fields)
                line_num += 1

                # Проверка на прогресс (если скрипт выводит "PROGRESS: XX%")
                if 'PROGRESS:' in line:
                    try:
                        progress = int(line.split('PROGRESS:')[1].split('%')[0].strip())
                        processing.progress = progress
                        processing.save(update_fields=['progress'])
                        _send_run_update(run_id, ProcessingStatus.RUNNING, progress=progress)
                    except (ValueError, IndexError):
                        pass

                # Проверка на текущий шаг
                if 'STEP:' in line:
                    try:
                        step = line.split('STEP:')[1].strip()
                        processing.current_step = step
                        processing.save(update_fields=['current_step'])
                        _send_run_update(run_id, ProcessingStatus.RUNNING, current_step=step)
                    except IndexError:
                        pass

        process.stdout.close()
        return_code = process.wait()

        # Обработка результата
        if return_code == 0:
            processing.status = ProcessingStatus.COMPLETED
            processing.progress = 100
            processing.current_step = 'Завершено'
            # processing.output_path = output_dir
            _send_log_update(run_id, "✅ Выполнение завершено успешно", line=line_num)
            _send_run_update(run_id, ProcessingStatus.COMPLETED, progress=100)

            with open(log_file, 'a') as f:
                logger.warning(f"run_id - {run_id}")
                f.write(transform_redis_logs_stream_to_str(run_id))
                f.write("\n=== ЗАВЕРШЕНО УСПЕШНО ===\n")
        else:
            processing.status = ProcessingStatus.FAILED
            processing.error_message = f"Код возврата: {return_code}"
            _send_log_update(run_id, f"❌ Ошибка. Код возврата: {return_code}", line=line_num)
            _send_run_update(run_id, ProcessingStatus.FAILED, progress=processing.progress)

            with open(log_file, 'a') as f:
                logger.warning(f"run_id err - {run_id}")
                f.write(transform_redis_logs_stream_to_str(run_id))
                f.write(f"\n=== ЗАВЕРШЕНО С ОШИБКОЙ (код {return_code}) ===\n")

        processing.stopped_at = processing.completed_at = timezone.now()
        processing.save(update_fields=[
            'status', 'progress', 'current_step', 'error_message', 'output_path', 'completed_at', 'stopped_at'
        ])

    except ProcessingModel.DoesNotExist:
        logger.error(f"Запуск {run_id} не найден")
        return
    except FileNotFoundError as e:
        logger.error(f"[Run {run_id}] Скрипт не найден: {e}")
        processing.status = ProcessingStatus.FAILED
        processing.error_message = str(e)
        processing.completed_at = timezone.now()
        processing.save(update_fields=['status', 'error_message', 'completed_at'])
        _send_run_update(run_id, ProcessingStatus.FAILED, progress=processing.progress)
        _send_log_update(run_id, f"❌ Ошибка: {e}")
    except Exception as e:
        logger.exception(f"[Run {run_id}] Ошибка выполнения: {e}")
        processing.status = ProcessingStatus.FAILED
        processing.error_message = str(e)
        processing.completed_at = timezone.now()
        processing.save(update_fields=['status', 'error_message', 'completed_at'])
        _send_run_update(run_id, ProcessingStatus.FAILED, progress=processing.progress)
        _send_log_update(run_id, f"❌ Ошибка: {e}")
