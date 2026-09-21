from django.urls import re_path
from core.websocket import consumers


websocket_urlpatterns = [
    re_path(r'ws/runs/(?P<run_id>[0-9a-f-]+)/$', consumers.AlgorithmRunConsumer.as_asgi()),
    re_path(r'ws/files/download/$', consumers.FileDownloadConsumer.as_asgi()),
]