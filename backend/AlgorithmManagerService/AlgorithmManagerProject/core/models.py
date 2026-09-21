import uuid
from urllib.parse import urlsplit, urlunsplit

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User


class FileSource(models.TextChoices):
    """Источник файла."""

    LOCAL = 'local', 'Локальная загрузка'
    HTTP = 'http', 'HTTP(S)'
    FTP = 'ftp', 'FTP'


class DownloadStatus(models.TextChoices):
    """Статус загрузки файла (для файлов по FTP/HTTP)."""

    QUEUED = 'queued', 'В очереди'
    DOWNLOADING = 'downloading', 'Скачивается'
    COMPLETED = 'completed', 'Готово'
    FAILED = 'failed', 'Ошибка'


class InputFileModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=500, verbose_name="Имя файла")
    filename = models.FileField(upload_to='input_files/%Y/%m/%d/', null=True, blank=True, verbose_name="Файл")
    file_size = models.BigIntegerField(default=0, verbose_name="Размер файла (байт)")
    checksum = models.CharField(max_length=64, blank=True, verbose_name="Контрольная сумма")
    is_deleted = models.BooleanField(default=False, verbose_name="Удален")
    source = models.CharField(max_length=10, choices=FileSource.choices, default=FileSource.LOCAL,
                              verbose_name="Источник")
    source_url = models.CharField(max_length=1024, blank=True, default="", verbose_name="Исходный URL")
    ftp_username = models.CharField(max_length=255, blank=True, default="", verbose_name="FTP логин")
    ftp_password = models.CharField(max_length=1024, blank=True, default="", verbose_name="FTP пароль (signed)")
    download_status = models.CharField(max_length=20, choices=DownloadStatus.choices,
                                       default=DownloadStatus.COMPLETED, verbose_name="Статус загрузки")
    download_error = models.TextField(blank=True, default="", verbose_name="Ошибка загрузки")
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Загрузивший")

    class Meta:
        db_table = 'input_file'
        ordering = ['-uploaded_at']
        verbose_name = 'Входной файл'
        verbose_name_plural = 'Входные файлы'

    def __str__(self):
        return self.name

    def get_file_size_mb(self):
        return round(self.file_size / (1024 * 1024), 2)

    @property
    def is_remote(self):
        return self.source in (FileSource.HTTP, FileSource.FTP)

    @property
    def display_url(self):
        """source_url без пароля (для отображения в UI/API)."""
        if not self.source_url:
            return ''
        try:
            p = urlsplit(self.source_url)
        except ValueError:
            return self.source_url
        if p.password:
            netloc = f"{p.username}:***@{p.hostname}" + (f":{p.port}" if p.port else '')
        else:
            netloc = p.netloc
        return urlunsplit((p.scheme, netloc, p.path, p.query, p.fragment))


class AlgorithmModel(models.Model):
    name = models.CharField(max_length=500, verbose_name="Имя алгоритма")
    description = models.TextField(blank=True, verbose_name="Описание алгоритма")
    version = models.CharField(max_length=50, default='1.0.0', verbose_name="Версия")
    is_active = models.BooleanField(default=True, verbose_name="Активен")
    script_path = models.CharField(max_length=500, verbose_name="Путь до скрипта")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    max_parallel_processes = models.PositiveSmallIntegerField(
        default=1,
        verbose_name="Макс. количество параллельных процесов для выполняемых, используя алгоритм")

    class Meta:
        db_table = "algorithm"
        verbose_name = 'Алгоритм'
        verbose_name_plural = 'Алгоритмы'

    def __str__(self):
        return self.name


class ArgType(models.TextChoices):
    VALUE = 'value', 'Значение (текст)'
    FILE_ARG = 'file_arg', 'Файл'
    FILE = 'file', 'Файл (без аргумента)'
    FLAG = 'flag', 'Флаг (без значения)'


class AlgorithmOptionModel(models.Model):
    algorithm = models.ForeignKey(AlgorithmModel, on_delete=models.CASCADE, verbose_name="Алгоритм")
    name = models.CharField(max_length=150, verbose_name="Имя опции алгоритма")
    description = models.TextField(blank=True, verbose_name="Описание алгоритма")
    option = models.CharField(max_length=50, verbose_name="Опция для алгоритма")
    example_value = models.CharField(max_length=255, blank=True, null=True, verbose_name="Пример значения")
    arg_type = models.CharField(max_length=10, choices=ArgType.choices, default=ArgType.VALUE,
                                verbose_name="Тип значения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        db_table = "algorithm_options"
        verbose_name = 'Опция алгорита'
        verbose_name_plural = 'Опции алгоритма'

    def __str__(self):
        return f"{self.name} ({self.option})"


class ProcessingStatus(models.TextChoices):
    """Статусы запуска алгоритма."""
    PENDING = 'pending', 'Ожидает запуска'
    QUEUED = 'queued', 'В очереди'
    RUNNING = 'running', 'Выполняется'
    COMPLETED = 'completed', 'Завершён успешно'
    FAILED = 'failed', 'Завершён с ошибкой'
    CANCELLED = 'cancelled', 'Отменён'


class ProcessingModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    algorithm = models.ForeignKey(AlgorithmModel, related_name='processing', on_delete=models.CASCADE,
                                  verbose_name="Алгоритм")
    output_path = models.CharField(max_length=500, blank=True, verbose_name="Директория результата")
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="Пользователь")
    status = models.CharField(max_length=20, choices=ProcessingStatus.choices, default=ProcessingStatus.PENDING,
                              verbose_name="Статус")
    progress = models.IntegerField(default=0, verbose_name="Прогресс (%)")
    current_step = models.CharField(max_length=255, blank=True, verbose_name="Текущий шаг")
    log_file = models.FilePathField(max_length=500, path='media/logs', null=True, blank=True, verbose_name="Путь к логу")
    celery_task_id = models.CharField(max_length=255, blank=True, verbose_name="ID задачи Celery")
    error_message = models.TextField(blank=True, verbose_name="Сообщение об ошибке")
    use_sudo = models.BooleanField(default=False, verbose_name="Запускать с sudo",
                                   help_text="Выполнять скрипт с префиксом sudo и выбранными опциями sudo")

    started_at = models.DateTimeField(null=True, blank=True, verbose_name="Начало выполнения")
    stopped_at = models.DateTimeField(null=True, blank=True, verbose_name="Конец выполнения")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Завершение")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        db_table = "processing"
        ordering = ['-created_at']
        verbose_name = 'Запуск алгоритма'
        verbose_name_plural = 'Запуски алгоритмов'

    def __str__(self):
        return f"Run {self.id} - {self.algorithm.name} ({self.status})"

    @property
    def duration_seconds(self):
        """Длительность выполнения в секундах."""

        if self.started_at and self.status not in [ProcessingStatus.CANCELLED, ProcessingStatus.COMPLETED, ProcessingStatus.CANCELLED]:
            end_time = self.completed_at or timezone.now()
            return abs(int((end_time - self.started_at).total_seconds()))
        elif self.stopped_at and self.status in [ProcessingStatus.CANCELLED, ProcessingStatus.COMPLETED, ProcessingStatus.CANCELLED]:
            return abs(int((self.stopped_at - self.started_at).total_seconds()))

        return 0

    def get_status_display_color(self):
        """Цвет для отображения статуса."""
        colors = {
            'pending': 'gray',
            'queued': 'blue',
            'running': 'green',
            'completed': 'success',
            'failed': 'red',
            'cancelled': 'orange',
        }
        return colors.get(self.status, 'gray')


class ProcessingArgOptionModel(models.Model):
    processing = models.ForeignKey(ProcessingModel, related_name='arguments', on_delete=models.CASCADE,
                                   verbose_name="Запуск")
    input_file = models.ForeignKey(InputFileModel, null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name='processing_arguments', verbose_name="Файл",
                                   help_text="Файл из системы, выбранный как значение аргумента")
    argument_order = models.PositiveSmallIntegerField(default=0, verbose_name="Позиция",
                                                help_text="Позиция аргумента в командной строке (порядок из формы)")
    value = models.CharField(max_length=1024, blank=True, default='', verbose_name="Значение",
                             help_text="Текстовое значение или путь к файлу (снапшот на момент запуска)")
    option = models.CharField(max_length=50, verbose_name="Опция для алгоритма")
    arg_type = models.CharField(max_length=10, choices=ArgType.choices, default=ArgType.VALUE,
                                verbose_name="Тип значения")
    use_sudo = models.BooleanField(default=False, verbose_name="Запускать с sudo",
                                   help_text="Выполнять скрипт с префиксом sudo и выбранными опциями sudo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        db_table = "processing_arg_option"
        ordering = ['argument_order']
        verbose_name = 'Аргумент запуска'
        verbose_name_plural = 'Аргументы запуска'

    def __str__(self):
        if self.value:
            return f"{self.option} {self.value}"
        return self.option
