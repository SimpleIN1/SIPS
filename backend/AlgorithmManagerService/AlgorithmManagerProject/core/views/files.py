import hashlib
import logging
import os
from urllib.parse import urlsplit

from django.db.models import Count
from django.contrib import messages
from django.http import FileResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import View, ListView, CreateView, UpdateView, DetailView

from core.dynamic_preferences_registry import global_pref
from core.dynamic_preferences_settings import DynamicPreferencesGeneralSection
from core.services import downloader
from celery_app.tasks import download_file_task
from core.forms.files import InputFileForm, RemoteFileUploadForm
from core.models import InputFileModel, FileSource, DownloadStatus


class InputFileListView(LoginRequiredMixin, ListView):
    model = InputFileModel
    queryset = InputFileModel.objects\
        .select_related('user')\
        .order_by('-uploaded_at')\
        .only('user__username', 'name', 'filename', 'file_size', 'source', 'download_status', 'is_deleted',
              'uploaded_at', 'checksum', 'download_error')
    context_object_name = "files"
    template_name = "core/files_list.html"
    paginate_by = 10


class InputFileDetailView(LoginRequiredMixin, DetailView):
    template_name = 'core/file_detail.html'
    queryset = InputFileModel.objects.select_related('user')
    context_object_name = 'file'


class InputFileUploadCreateView(LoginRequiredMixin, CreateView):
    model = InputFileModel
    form_class = InputFileForm
    template_name = "core/files_upload.html"
    success_url = reverse_lazy('core:files_list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.name = self.request.FILES['filename'].name
        self.object.file_size = self.request.FILES['filename'].size
        self.object.save()
        messages.success(self.request, 'Файл загружен')
        return super().form_valid(form)


class InputFileUploadRemoteView(LoginRequiredMixin, View):
    template_name = "core/files_upload.html"
    form_class = RemoteFileUploadForm

    def get(self, request):
        form = self.form_class()
        form.max_links = global_pref[DynamicPreferencesGeneralSection(True).max_links_remote_download]
        context = {
            "form": form,
            'remote': True,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        form.max_links = global_pref[DynamicPreferencesGeneralSection(True).max_links_remote_download]

        context = {
            "form": form,
            'remote': True,
        }

        if form.is_valid():
            links = form.cleaned_data['links']
            ftp_username = (form.cleaned_data.get('ftp_username') or '').strip()
            ftp_password = form.cleaned_data.get('ftp_password') or ''

            created_ids = []
            for url in links:
                scheme = urlsplit(url).scheme.lower()
                is_ftp = scheme in ('ftp', 'ftps')
                obj = InputFileModel(
                    name=downloader.derive_filename(url),
                    file_size=0,
                    user=request.user,
                    source=FileSource.FTP if is_ftp else FileSource.HTTP,
                    source_url=url,
                    ftp_username=ftp_username,
                    ftp_password=downloader.sign_secret(ftp_password) if is_ftp else '',
                    download_status=DownloadStatus.QUEUED,
                )
                obj.save()
                created_ids.append(str(obj.id))

            for fid in created_ids:
                download_file_task.delay(fid)

            messages.success(request, f'В очередь на скачивание поставлено файлов: {len(created_ids)}')

            return redirect('core:files_list')

        return render(request, self.template_name, context)


class InputFileDeleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        """Удаление файла: запись + файл на диске.

        Защита:
        - нельзя удалить, пока идёт скачивание (воркер может дописывать файл);
        - нельзя удалить, если файл используется в запусках (у AlgorithmRun.input_file
          on_delete=CASCADE — удаление затерло бы и историю запусков).
        """
        file = get_object_or_404(InputFileModel, pk=pk)
        name = file.name

        if file.download_status in (DownloadStatus.QUEUED, DownloadStatus.DOWNLOADING):
            messages.warning(request, f'Файл «{name}» ещё скачивается — удаление возможно после завершения.')
            return redirect('core:files_list')

        # Удаляем файл с диска, затем запись. Ошибки удаления файла не блокируют удаление записи.
        if file.filename:
            try:
                file.filename.delete(save=False)
            except Exception as e:
                messages.error(request, f'Файл на диске не удалён: {e}. Запись будет удалена.')

        file.is_deleted = True
        file.save()

        messages.success(request, f'Файл «{name}» удалён')
        return redirect('core:files_list')


class InputFileRetryDownload(LoginRequiredMixin, View):
    def post(self, request, pk):
        file = get_object_or_404(InputFileModel, pk=pk)
        if not file.is_remote:
            messages.error(request, 'Файл не является удалённым (FTP/HTTP)')
            return redirect('core:files_list')
        if file.download_status == DownloadStatus.COMPLETED:
            messages.info(request, 'Файл уже скачан, повтор не требуется')
            return redirect('core:files_list')

        file.download_status = DownloadStatus.QUEUED
        file.download_error = ''
        file.save(update_fields=['download_status', 'download_error'])
        download_file_task.delay(str(file.id))
        messages.success(request, 'Скачивание повторяется')
        return redirect('core:files_list')


class InputFileCalculateChecksumView(LoginRequiredMixin, View):
    def post(self, request, pk):
        file = get_object_or_404(InputFileModel, pk=pk)

        checksum = hashlib.sha256()
        with file.file.open('rb') as f:
            for chunk in iter(lambda: f.read(8192), b''):
                checksum.update(chunk)

        file.checksum = checksum.hexdigest()
        file.save(update_fields=['checksum'])

        messages.success(request, f'Checksum вычислен: {file.checksum[:16]}...')
        return redirect('core:files_list')


class InputFileDownloadView(LoginRequiredMixin, View):
    def get(self, request, pk):
        file_input = get_object_or_404(InputFileModel, pk=pk)

        if not os.path.exists(file_input.filename.path):
            return redirect("not-found")

        return FileResponse(open(file_input.filename.path, "rb"))
