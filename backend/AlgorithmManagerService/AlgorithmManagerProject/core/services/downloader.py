"""
Скачивание удалённых файлов (HTTP/HTTPS и FTP/FTPS) на диск.

Используется Celery-задачей download_file_task для загрузки h5-файлов по ссылкам.
Секреты (FTP-пароль) подписываются/восстанавливаются через django.core.signing.
"""
import os
import ssl
import logging
import posixpath
import urllib.error
import urllib.request
from urllib.parse import unquote, urlsplit
from ftplib import FTP, all_errors, FTP_TLS

from django.conf import settings
from django.core import signing

logger = logging.getLogger(__name__)

_FTP_PASSWORD_SALT = 'algmanager.ftp-password'


class DownloadError(Exception):
    """Ошибка скачивания файла (читаемое сообщение для download_error)."""
    pass


def sign_secret(value: str) -> str:
    """Обратимо-подписанное представление секрета (не plaintext в БД)."""
    if not value:
        return ''
    return signing.dumps(value, salt=_FTP_PASSWORD_SALT)


def verify_secret(token: str) -> str:
    """Восстановление секрета из подписанного представления."""
    if not token:
        return ''
    try:
        return signing.loads(token, salt=_FTP_PASSWORD_SALT)
    except signing.BadSignature:
        return ''


def derive_filename(url: str, fallback: str = 'download.h5') -> str:
    """Имя файла из URL (basename пути, без query/фрагмента)."""
    try:
        name = posixpath.basename(urlsplit(url).path)
        name = unquote(name).strip()
    except (ValueError, AttributeError):
        name = ''
    return name or fallback


def _default_max_size() -> int:
    return int(getattr(settings, 'MAX_UPLOAD_SIZE', 2 * 1024 * 1024 * 1024))


def _download_http(url: str, dest_path: str, max_size: int) -> None:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'AlgManager/1.0'})
        resp = urllib.request.urlopen(req, timeout=300)
    except urllib.error.HTTPError as e:
        raise DownloadError(f'HTTP ошибка: {e.code} {e.reason}') from e
    except (urllib.error.URLError, OSError, ValueError) as e:
        reason = getattr(e, 'reason', None)
        raise DownloadError(f'HTTP ошибка: {reason or e}') from e

    written = 0
    try:
        with open(dest_path, 'wb') as fh:
            while True:
                chunk = resp.read(1024 * 1024)
                if not chunk:
                    break
                written += len(chunk)
                if written > max_size:
                    raise DownloadError(f'Файл превышает лимит {max_size} байт')
                fh.write(chunk)
    except OSError as e:
        raise DownloadError(f'Ошибка записи файла: {e}') from e
    finally:
        resp.close()


def _download_ftp(url: str, split, dest_path: str, username: str, password: str, max_size: int) -> None:

    host = split.hostname
    if not host:
        raise DownloadError('FTP: не указан хост')
    port = split.port or 21

    # Приоритет: креденшелы в URL -> переданные из формы -> anonymous
    user = split.username or username or 'anonymous'
    pwd = split.password or password or ''
    if not pwd and user != 'anonymous':
        pwd = ''

    remote_dir = posixpath.dirname(split.path)
    remote_name = posixpath.basename(unquote(split.path))
    if not remote_name:
        raise DownloadError('FTP: не удалось определить имя файла в пути')

    if (split.scheme or '').lower() == 'ftps':
        client = FTP_TLS(context=ssl.create_default_context())
    else:
        client = FTP()

    try:
        client.connect(host, port, timeout=30)
        client.login(user, pwd)
        client.set_pasv(True)
        if remote_dir and remote_dir != '/':
            client.cwd(remote_dir)

        # Ранняя проверка размера (команда SIZE может не поддерживаться)
        try:
            remote_size = client.size(remote_name)
        except all_errors:
            remote_size = None
        if remote_size is not None and remote_size > max_size:
            raise DownloadError(f'Файл на сервере ({remote_size} байт) превышает лимит {max_size} байт')

        state = {'written': 0}

        def _handle(chunk: bytes) -> None:
            state['written'] += len(chunk)
            if state['written'] > max_size:
                raise DownloadError(f'Файл превышает лимит {max_size} байт')
            fh.write(chunk)

        with open(dest_path, 'wb') as fh:
            client.retrbinary(f'RETR {remote_name}', _handle)
    except DownloadError:
        raise
    except all_errors as e:
        raise DownloadError(f'FTP ошибка: {e}') from e
    except OSError as e:
        raise DownloadError(f'Ошибка записи файла: {e}') from e
    finally:
        try:
            client.quit()
        except all_errors:
            pass


def download_to_disk(url: str, dest_path: str, username: str = '', password: str = '') -> int:
    """
    Скачать удалённый файл по HTTP(S)/FTP(S) в dest_path.

    Возвращает количество записанных байт.
    Бросает DownloadError при ошибке или превышении лимита.
    """
    max_size = _default_max_size()
    split = urlsplit(url)
    scheme = (split.scheme or '').lower()

    if scheme in ('http', 'https'):
        _download_http(url, dest_path, max_size)
    elif scheme in ('ftp', 'ftps'):
        _download_ftp(url, split, dest_path, username, password, max_size)
    else:
        raise DownloadError(f'Неподдерживаемый протокол: {scheme or "не указан"}')

    size = os.path.getsize(dest_path)
    if size > max_size:
        try:
            os.remove(dest_path)
        except OSError:
            pass
        raise DownloadError(f'Файл ({size} байт) превышает лимит {max_size} байт')
    return size
