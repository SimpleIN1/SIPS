from __future__ import annotations

from datetime import datetime

from django.conf import settings
from django.db import transaction
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.sessions.backends.cache import SessionStore # cache

from AccountApp.services.mail.mail_context import ConfirmationEmail, ResetPasswordEmail
from AccountApp.services.manage_datetime import is_expiration_time


UserModel = get_user_model()


def send_confirmation_email(user: UserModel) -> None:
    s = SessionStore()
    data = {
        settings.CACHE_VERIFY_REGISTER_EMAIL: {
            "verify": False,
            "datetime_created": str(datetime.now().timestamp()).split('.')[0],
            "user_id": user.id
        }
    }
    s.update(data)
    s.save()

    # send email
    verify_url = f"{settings.SCHEMA}://{settings.DOMAIN}:{settings.PORT}{reverse_lazy('email-verify', kwargs={'sessionid': s.session_key})}"
    # print(f"verify_url: {verify_url}, email: {user.email}")
    context = {
        "verify_url": verify_url
    }
    ConfirmationEmail(email=user.email, context=context).send()


def confirm_email(session_id: str) -> int | None:
    s = SessionStore(session_id)
    if not s.exists(session_id):
        return None

    data = s.get(settings.CACHE_VERIFY_REGISTER_EMAIL)
    if not data:
        return None

    if not is_expiration_time(data["datetime_created"], settings.NOTIFY_EXPIRATION_MINUTES):
        return None

    verify = data.get("verify")
    if verify is None:
        return None

    if verify == True:
        return None

    with transaction.atomic():
        UserModel.objects.filter(id=data["user_id"]).update(is_active=True, is_verify=True)
    s.delete(session_id)

    return data.get("user_id")


def send_reset_password_email(user: UserModel) -> None:

    s = SessionStore()
    data = {
        settings.CACHE_PASSWORD_RESET_EMAIL: {
            "reset": False,
            "datetime_created": str(datetime.now().timestamp()).split('.')[0],
            "user_id": user.id
        }
    }
    s.update(data)
    s.save()

    # send email
    password_reset_url = f"{settings.URL_FRONTEND_RESET_PASSWORD}?sessionid={s.session_key}"
    # print(f"password_reset_url: {password_reset_url}, email: {user.email}")
    context = {
        "password_reset_url": password_reset_url
    }
    ResetPasswordEmail(email=user.email, context=context).send()


def confirm_reset_password_email(session_id: str) -> int | None:
    s = SessionStore(session_id)
    if not s.exists(session_id):
        return None

    data = s.get(settings.CACHE_PASSWORD_RESET_EMAIL)
    if not data:
        return None

    if not is_expiration_time(data["datetime_created"], settings.NOTIFY_EXPIRATION_MINUTES):
        return None

    reset = data.get("reset")
    if reset is None:
        return None

    if reset == True:
        return None

    s.delete(session_id)
    return data["user_id"]

