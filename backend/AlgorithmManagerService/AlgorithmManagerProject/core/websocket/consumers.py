import json
import logging
import pprint

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async

from core.models import ProcessingModel, ProcessingStatus
from core.services.redis_service import async_redis_client
from core.services.monitor_logger import get_all_logs_stream


class AlgorithmRunConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer для мониторинга выполнения алгоритма в реальном времени.

    Подключение: ws://host:port/ws/runs/<run_id>/

    Сообщения от сервера:
    - {"type": "status_update", "status": "running", "progress": 50, "current_step": "..."}
    - {"type": "all_logs_stream", "messages": [{"line": 1, "message": "Log", "class": "log-success"}]}
    - {"type": "log_update", "message": "..."}
    - {"type": "completed", "status": "completed", "output_path": "..."}
    - {"type": "error", "message": "..."}
    """

    async def connect(self):
        self.run_id = self.scope['url_route']['kwargs']['run_id']
        self.room_group_name = f'run_{self.run_id}'

        # Проверка существования запуска
        run_exists = await self.run_exists(self.run_id)
        if not run_exists:
            await self.close()
            return

        # Присоединение к группе
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Отправка текущего статуса при подключении
        current_status = await self.get_current_status(self.run_id)

        if current_status["status"] not in [ProcessingStatus.FAILED,
                                            ProcessingStatus.COMPLETED,
                                            ProcessingStatus.CANCELLED]:
            # Получение логов из редиса
            logs = await get_all_logs_stream(self.run_id)
            # Отправка их на клинет
            await self.send_all_logs_stream(logs)

        if current_status:
            await self.send(text_data=json.dumps(current_status))

    async def disconnect(self, close_code):
        # Отключение от группы
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Получение сообщений от клиента."""
        data = json.loads(text_data)
        action = data.get('action')

        if action == 'subscribe':
            # Подписка на обновления
            pass
        elif action == 'unsubscribe':
            # Отписка
            await self.close()

    async def send_status_update(self, event):
        """Отправка обновления статуса."""
        await self.send(text_data=json.dumps({
            'type': 'status_update',
            'status': event['status'],
            'progress': event.get('progress', 0),
            'current_step': event.get('current_step', ''),
            'error_message': event.get('error_message', ''),
        }))

    async def send_log_update(self, event):
        """Отправка обновления лога."""
        await self.send(text_data=json.dumps({
            'type': 'log_update',
            'message': event['message'],
            'class': event.get('class', ''),
            'line': event.get('line', 0),
        }))

    async def send_all_logs_stream(self, event):
        await self.send(text_data=json.dumps({
            'type': 'all_logs_stream',
            'messages': event['messages'],
        }))

    async def send_completed(self, event):
        """Отправка уведомления о завершении."""
        await self.send(text_data=json.dumps({
            'type': 'completed',
            'status': event['status'],
            'output_path': event.get('output_path', ''),
            'duration': event.get('duration', 0),
        }))

    async def send_error(self, event):
        """Отправка уведомления об ошибке."""
        await self.send(text_data=json.dumps({
            'type': 'error',
            'message': event['message'],
        }))

    @database_sync_to_async
    def run_exists(self, run_id):
        """Проверка существования запуска."""
        return ProcessingModel.objects.filter(id=run_id).exists()

    @database_sync_to_async
    def get_current_status(self, run_id):
        """Получение текущего статуса."""
        try:
            run = ProcessingModel.objects.select_related('algorithm').get(id=run_id)
            return {
                'type': 'status_update',
                'run_id': str(run.id),
                'algorithm_name': run.algorithm.name,
                'status': run.status,
                'progress': 12 or run.progress,
                'current_step': "current step" or run.current_step,
                'started_at': run.started_at.isoformat() if run.started_at else None,
            }
        except ProcessingModel.DoesNotExist:
            return None


class FileDownloadConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer для живого статуса загрузки файлов (HTTP/FTP).

    Подключение: ws://host/ws/files/download/
    Группируется по пользователю: files_user_<user_id>.

    Сообщения от сервера:
    - {"type": "file_download_status", "file_id": ..., "status": ..., "status_display": ..., "file_size_mb": ..., "error": ...}
    - {"type": "file_download_status_batch", "files": [ {...}, ... ]} — текущие статусы при подключении
    """

    async def connect(self):
        self.room_group_name = None
        user = self.scope.get('user')
        if user is None or not user.is_authenticated:
            await self.close(code=4401)
            return

        self.room_group_name = f'files_user_{user.id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Синхронизация: отправляем текущие незавершённые статусы файлов пользователя
        files = await self.get_user_file_statuses(user.id)
        await self.send(text_data=json.dumps({
            'type': 'file_download_status_batch',
            'files': files,
        }))

    async def disconnect(self, close_code):
        if self.room_group_name:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def send_file_download_status(self, event):
        """Отправка обновления статуса одного файла."""
        await self.send(text_data=json.dumps({
            'type': 'file_download_status',
            'file_id': event['file_id'],
            'status': event['status'],
            'status_display': event['status_display'],
            'file_size_mb': event.get('file_size_mb', 0),
            'is_remote': event.get('is_remote', False),
            'error': event.get('error', ''),
        }))

    @database_sync_to_async
    def get_user_file_statuses(self, user_id):
        """Незавершённые загрузки файлов пользователя (queued/downloading/failed)."""
        from core.models import InputFileModel, DownloadStatus
        files = InputFileModel.objects.filter(user_id=user_id).exclude(
            download_status=DownloadStatus.COMPLETED
        )
        return [
            {
                'file_id': str(f.id),
                'status': f.download_status,
                'status_display': f.get_download_status_display(),
                'file_size_mb': f.get_file_size_mb(),
                'error': f.download_error or '',
            }
            for f in files
        ]
