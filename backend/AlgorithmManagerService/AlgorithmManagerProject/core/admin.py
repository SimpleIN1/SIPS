from django.contrib import admin
from core.models import AlgorithmModel, InputFileModel, ProcessingModel, AlgorithmOptionModel, ProcessingArgOptionModel


@admin.register(AlgorithmModel)
class AlgorithmAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    ordering = ('name',)


@admin.register(InputFileModel)
class InputFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_file_size_mb', 'uploaded_at', 'user')
    list_filter = ('uploaded_at', )
    search_fields = ('original_filename',)
    readonly_fields = ('id', 'file_size', 'checksum')
    ordering = ('-uploaded_at',)


@admin.register(ProcessingModel)
class ProcessingAdmin(admin.ModelAdmin):
    list_display = ('id', 'algorithm', 'status', 'started_at', 'completed_at', 'duration_seconds', )
    list_filter = ('status', 'algorithm', 'created_at')
    search_fields = ('id', 'algorithm__name')
    readonly_fields = ('id', 'celery_task_id', 'duration_seconds', )
    ordering = ('-created_at',)


@admin.register(AlgorithmOptionModel)
class AlgorithmOptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'option', 'algorithm', 'example_value', 'created_at')
    search_fields = ('name', 'description', 'option')
    ordering = ('name',)


@admin.register(ProcessingArgOptionModel)
class ProcessingArgOptionModelAdmin(admin.ModelAdmin):
    list_display = ('processing', 'input_file', 'value', 'option', 'arg_type', 'created_at')
    ordering = ('created_at',)
