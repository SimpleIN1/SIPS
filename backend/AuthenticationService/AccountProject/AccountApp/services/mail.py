
import pickle
from typing import TYPE_CHECKING, Any, Dict, Optional

from django.conf import settings
from rest_framework.request import Request
import rest_registration.notifications.email
from django.core.mail.message import EmailMultiAlternatives
from rest_registration.verification_notifications import send_reset_password_verification_email_notification
from rest_registration.notifications.enums import NotificationMethod, NotificationType

if TYPE_CHECKING:
    from django.contrib.auth.base_user import AbstractBaseUser

from CeleryApp.tasks import send_email_with_broker


def build_default_template_context(  # для контекста
        user: 'AbstractBaseUser',
        user_address: Any,
        data: Dict[str, Any],
        notification_type: Optional[NotificationType] = None,
        notification_method: Optional[NotificationMethod] = None) -> Dict[str, Any]:
    context = {
        'user': user,
        'email': user_address,
        'site_name': settings.WEBSITE_NAME
    }
    data = data.copy()
    params_signer = data.pop('params_signer', None)
    if params_signer:
        context['verification_url'] = params_signer.get_url()
    context.update(data)
    return context


def send_reset_password_verification_email_notification_custom(
        request: Request,
        user: 'AbstractBaseUser',
) -> None:
    send_reset_password_verification_email_notification(request, user)


def send_notification(notification: EmailMultiAlternatives) -> None:
    notification_pickle = pickle.dumps(notification)
    send_email_with_broker.delay(notification_pickle)


rest_registration.notifications.email.send_notification = send_notification
