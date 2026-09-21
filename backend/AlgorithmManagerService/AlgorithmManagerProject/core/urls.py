from django.urls import path
from django.views.generic.base import TemplateView

from core.views import (dashboard as dash_view,
                        account as acc_view,
                        algorithm as alg_view,
                        files as f_view,
                        processing as p_view)

app_name = 'core'

urlpatterns = [
    path('', dash_view.DashboardView.as_view(), name="dashboard"),

    path('algorithms/', alg_view.AlgorithmListView.as_view(), name="algorithms_list"),
    path('algorithms/create/', alg_view.AlgorithmCreateView.as_view(), name="algorithm_create"),
    path('algorithms/<int:pk>/', alg_view.AlgorithmUpdateView.as_view(), name='algorithm_update'),

    path('files/', f_view.InputFileListView.as_view(), name="files_list"),
    path('files/upload/', f_view.InputFileUploadCreateView.as_view(), name="file_upload"),
    path('files/upload-remote/', f_view.InputFileUploadRemoteView.as_view(), name='file_upload_remote'),
    path('files/<uuid:pk>/', f_view.InputFileDetailView.as_view(), name='file_detail'),
    path('files/<uuid:pk>/delete/', f_view.InputFileDeleteView.as_view(), name='file_delete'),
    path('files/<uuid:pk>/checksum/', f_view.InputFileCalculateChecksumView.as_view(), name='file_calculate_checksum'),
    path('files/<uuid:pk>/retry-download/', f_view.InputFileRetryDownload.as_view(), name='file_retry_download'),
    path('files/<uuid:pk>/download-file/', f_view.InputFileDownloadView.as_view(), name='file_download'),

    path('processing/', p_view.ProcessingListView.as_view(), name="processing_list"),
    path('processing/create/', p_view.ProcessingCreateView.as_view(), name="processing_create"),
    path('processing/<uuid:pk>/', p_view.ProcessingDetailView.as_view(), name='processing_detail'),
    path('processing/<uuid:pk>/monitor/', p_view.ProcessingMonitorView.as_view(), name='processing_monitor'),
    path('processing/<uuid:pk>/monitor/status/', p_view.ProcessingMonitorStatusView.as_view(), name='processing_monitor_status'),
    path('processing/<uuid:pk>/monitor/logs/', TemplateView.as_view(content_type='text/plain'), name='processing_monitor_logs'),
    path('processing/<uuid:pk>/cancel/', p_view.ProcessingCancelView.as_view(), name='processing_cancel'),
    path('processing/<uuid:pk>/download-logfile/', p_view.ProcessingDownloadLogFileView.as_view(), name='processing_download_logfile'),

    path('login/', acc_view.LoginView.as_view(), name="login"),
    path('logout/', acc_view.LogoutView.as_view(), name="logout"),
    path('profile/', acc_view.ProfileView.as_view(), name="profile"),

]
