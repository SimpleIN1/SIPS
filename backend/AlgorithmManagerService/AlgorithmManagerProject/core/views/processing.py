import os
import pprint
import re
import json
import logging
from pathlib import Path

from django.http import FileResponse
from django.utils import timezone
from django.db import models
from django.contrib import messages
from django_filters.views import FilterView
from django_filters import FilterSet, CharFilter
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View, ListView, CreateView, UpdateView, DetailView

from core.services import downloader
from celery.result import AsyncResult
from core.forms.processing import ProcessingForm
from core.forms.files import InputFileForm, RemoteFileUploadForm
from celery_app.tasks import download_file_task, run_algorithm_task
from core.models import AlgorithmModel, ProcessingModel, InputFileModel, ProcessingStatus, ProcessingArgOptionModel, \
    AlgorithmOptionModel, ArgType
from core.services.monitor_logger import transform_redis_logs_stream_to_str, get_type_line

logger = logging.getLogger(__name__)


class ProcessingModelFilterSet(FilterSet):
    class Meta:
        model = ProcessingModel
        fields = ['log_file', 'status', 'algorithm']

        filter_overrides = {
            models.FileField: {
                'filter_class': CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }


class ProcessingListView(LoginRequiredMixin, FilterView):
    model = ProcessingModel
    template_name = 'core/processing_list.html'
    context_object_name = 'runs'
    queryset = ProcessingModel.objects\
        .select_related('algorithm')\
        .order_by('-created_at')\
        .only('algorithm__name', 'status', 'progress', 'created_at', 'completed_at', 'started_at', 'stopped_at')

    paginate_by = 30
    filterset_class = ProcessingModelFilterSet

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        algorithms = AlgorithmModel.objects.all()
        context['algorithms'] = algorithms
        return context


def _transform_algorithm_options_to_json(context):
    algorithm_option = list(AlgorithmOptionModel.objects.select_related("algorithm")
                            .filter(algorithm__is_active=True)\
                            .only('algorithm__is_active', 'name', 'option', 'description', 'example_value', 'arg_type'))
    options_data = {}
    for op in algorithm_option:
        key = str(op.algorithm.id)
        options_data.setdefault(key, [])
        options_data[key].append({
            'id': op.id,
            'name': op.name,
            'argument': op.option,
            'description': op.description,
            'value': op.example_value,
            'is_enabled': False,
            'is_boolean': op.arg_type == ArgType.FLAG
        })
    context['options_json'] = json.dumps(options_data)


def _transform_file_data_to_json(context):
    files_data = [
        {
            'id': str(f.id),
            'is_deleted': f.is_deleted,
            'name': f.name,
        }
        for f in InputFileModel.objects.order_by('-uploaded_at')
    ]
    context["files_json"] = json.dumps(files_data, ensure_ascii=False)


class ProcessingCreateView(LoginRequiredMixin, View):
    template_name = 'core/processing_form.html'
    from_class = ProcessingForm

    def get(self, request):
        context = {}
        form = self.from_class()
        if algorithm_id := request.GET.get('algorithm'):
            form.fields['algorithm'].initial = algorithm_id

        context["form"] = form

        # Получаем данные об опциях для каждого алгоритма
        logger.info("Получаем данные об опциях для каждого алгоритма")
        _transform_algorithm_options_to_json(context)

        # Список загруженных файлов для выбора как значения аргумента/опции
        logger.info("Список загруженных файлов для выбора как значения аргумента/опции")
        _transform_file_data_to_json(context)

        return render(request, self.template_name, context)

    def post(self, request):
        context = {}
        use_sudo = False
        form = self.from_class(request.POST)

        if form.is_valid():
            run = form.save(commit=False)
            run.status = ProcessingStatus.QUEUED
            run.user = self.request.user
            run.save()

            logger.info("Извлекаем доп аргументы из формы")

            # Получаем дополнительные аргументы из POST данных (строки extra_arg_0, extra_arg_1, ...)
            # Собираем все присутствующие индексы (устойчиво к удалению средних строк)
            extra_arg_indices = sorted({
                int(m.group(1))
                for key in request.POST.keys()
                if (m := re.match(r'^extra_arg_(\d+)$', key))
            })

            logger.info(f"Форматирование доп аргументов для сохранение в базу - {extra_arg_indices}")

            argument_rows = []
            for position, i in enumerate(extra_arg_indices):
                arg = request.POST.get(f'extra_arg_{i}', '').strip()
                arg_type = request.POST.get(f'extra_arg_type_{i}', 'value').strip() or 'value'

                if not arg and arg_type != ArgType.FILE:
                    continue
                if arg_type not in ArgType.values:
                    arg_type = ArgType.VALUE

                file_obj = None
                if arg_type in [ArgType.FILE_ARG, ArgType.FILE]:
                    file_id = request.POST.get(f'extra_arg_file_{i}', '').strip()
                    try:
                        file_obj = InputFileModel.objects.get(id=file_id)
                    except InputFileModel.DoesNotExist:
                        messages.error(request, f'Файл для аргумента "{arg}" не найден')

                if file_obj is not None:
                    value = file_obj.filename.path
                elif arg_type == ArgType.VALUE:
                    value = request.POST.get(f'extra_arg_value_{i}', '').strip()
                else:
                    value = ''

                # Флаг без значения или аргумент с значением
                if value or arg_type in [ArgType.FLAG, ArgType.FILE]:
                    argument_rows.append(ProcessingArgOptionModel(
                        processing=run,
                        argument_order=position,
                        option=arg,
                        arg_type=arg_type,
                        value=value,
                        input_file=file_obj,
                        use_sudo=False,
                    ))

            logger.info("Извлекаем sudo аргументы")
            # Получаем опции sudo из POST данных (строки sudo_arg_0, sudo_arg_1, ...)
            sudo_option_rows = []
            if run.use_sudo:
                sudo_arg_indices = sorted({
                    int(m.group(1))
                    for key in request.POST.keys()
                    if (m := re.match(r'^sudo_arg_(\d+)$', key))
                })
                for position, i in enumerate(sudo_arg_indices):
                    arg = request.POST.get(f'sudo_arg_{i}', '').strip()
                    arg_type = request.POST.get(f'sudo_arg_type_{i}', 'flag').strip() or 'flag'
                    if not arg:
                        continue
                    if arg_type not in ArgType.values:
                        arg_type = ArgType.FLAG

                    if arg_type == ArgType.VALUE:
                        value = request.POST.get(f'sudo_arg_value_{i}', '').strip()
                    else:
                        value = ''

                    sudo_option_rows.append(ProcessingArgOptionModel(
                        processing=run,
                        argument_order=position,
                        option=arg,
                        arg_type=arg_type,
                        value=value,
                        use_sudo=True,
                    ))

            logger.info("Сохранение аргументов в отдельной таблице")
            # Сохраняем доп. аргументы (отдельная таблица)
            if sudo_option_rows:
                use_sudo = True
                argument_rows += sudo_option_rows

            ProcessingArgOptionModel.objects.bulk_create(argument_rows)

            logger.info(f"Запуск обработки алгоритма {run.id}")

            # Запуск Celery задачи
            task = run_algorithm_task.delay(str(run.id))
            run.celery_task_id = task.id
            run.use_sudo = use_sudo
            run.save(update_fields=['celery_task_id', 'use_sudo'])

            messages.success(request, 'Запуск создан')

            return redirect('core:processing_monitor', pk=run.pk)

        context["form"] = form

        # Получаем данные об опциях для каждого алгоритма
        logger.info("Получаем данные об опциях для каждого алгоритма")
        _transform_algorithm_options_to_json(context)

        # Список загруженных файлов для выбора как значения аргумента/опции
        logger.info("Список загруженных файлов для выбора как значения аргумента/опции")
        _transform_file_data_to_json(context)

        return render(request, self.template_name, context)


class ProcessingMonitorView(LoginRequiredMixin, View):
    template_name = 'core/processing_monitor.html'

    def get(self, request, pk):
        run = get_object_or_404(
            ProcessingModel.objects.select_related('algorithm'),
            pk=pk
        )

        log_lines = []
        log_error = None

        if run.log_file:
            try:
                with open(run.log_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            # Определяем класс для стилизации
                            line_class = get_type_line(line)
                            log_lines.append({'text': line, 'class': line_class})
            except FileNotFoundError:
                log_error = 'Лог файл ещё не создан'
            except PermissionError:
                log_error = 'Нет доступа к файлу логов'
            except Exception as e:
                log_error = f'Ошибка чтения логов: {str(e)}'
        else:
            log_error = 'Лог файл не указан'

        return render(request, self.template_name, {
            'run': run,
            'log_lines': log_lines,
            'log_error': log_error
        })


class ProcessingDetailView(LoginRequiredMixin, View):
    template_name = "core/processing_detail.html"

    def get(self, request, pk):
        run = get_object_or_404(
            ProcessingModel.objects.select_related('algorithm', 'user'),
            pk=pk
        )

        # Load logs if available
        log_content = []
        if run.log_file:
            try:
                with open(run.log_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            log_content.append(line)
            except FileNotFoundError:
                pass

        return render(request, self.template_name, {'run': run, 'log_content': log_content})


class ProcessingMonitorStatusView(LoginRequiredMixin, DetailView):
    model = ProcessingModel
    template_name = 'core/partials/processing_status.html'
    context_object_name = 'run'


class ProcessingCancelView(LoginRequiredMixin, View):
    def post(self, request, pk):
        processing = get_object_or_404(ProcessingModel, pk=pk)

        if processing.status not in [ProcessingStatus.PENDING, ProcessingStatus.QUEUED, ProcessingStatus.RUNNING]:
            messages.error(request, f'Невозможно отменить запуск в статусе {processing.get_status_display()}')
        else:
            if processing.celery_task_id:
                task = AsyncResult(processing.celery_task_id)
                task.revoke(terminate=True)

            with open(processing.log_file, 'a') as f:
                f.write(transform_redis_logs_stream_to_str(pk))
                f.write(f"\n=== ЗАВЕРШЕНО С ОТМЕНОЙ ===\n")

            processing.status = ProcessingStatus.CANCELLED
            processing.stopped_at = timezone.now()
            processing.save(update_fields=['status', 'stopped_at'])
            messages.success(request, 'Запуск отменён')

        return redirect('core:processing_list')


class ProcessingDownloadLogFileView(LoginRequiredMixin, View):
    def get(self, request, pk):
        processing = get_object_or_404(ProcessingModel, pk=pk)

        if not os.path.exists(processing.log_file):
            return redirect("not-found")

        return FileResponse(open(processing.log_file, "rb"))
