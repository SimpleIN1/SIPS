
import pickle
import pprint
from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Any, Dict, Optional

from django.conf import settings
from django.core.mail.message import EmailMultiAlternatives

from rest_framework.request import Request
import rest_registration.notifications.email
from rest_registration.exceptions import APIException
from rest_registration.verification_notifications import (send_reset_password_verification_email_notification,
                                                          _get_email_template_config_data)
from rest_registration.notifications.email import send_verification_notification
from rest_registration.notifications.enums import NotificationMethod, NotificationType
from rest_registration.signers.register import RegisterSigner
from rest_registration.signers.register_email import RegisterEmailSigner
from rest_registration.signers.reset_password import ResetPasswordSigner
from rest_registration.utils.users import get_user_verification_id

from AccountApp.models import OTPUserModel
from AccountApp.services.common import NotificationTypeOTP
from AccountApp.views import OTPChecking

if TYPE_CHECKING:
    from django.contrib.auth.base_user import AbstractBaseUser

from django.conf import settings
from CeleryApp.tasks import send_email_with_broker
from AccountApp.services.code_generator import generate_code


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

    for key, value in data.items():
        context['key'] = value

    context.update(data)
    return context


# rest registartion + broker sending email link
def send_notification(notification: EmailMultiAlternatives) -> None:
    notification_pickle = pickle.dumps(notification)
    send_email_with_broker.delay(notification_pickle)


rest_registration.notifications.email.send_notification = send_notification


def make_otp_code_notification(
    user: 'AbstractBaseUser',
    notification_type_otp: NotificationTypeOTP
) -> int:
    otp_code = generate_code()
    datetime_now = datetime.now(tz=timezone.utc)
    item = OTPUserModel(
        user=user,
        otp_code=otp_code,
        expires=datetime_now + timedelta(minutes=settings.OTP_CODE_TIME_MINUTES),
        next_code_time=datetime_now + timedelta(minutes=settings.OTP_CODE_NEXT_TIME_MINUTES),
        notification_type_otp=notification_type_otp.value
    )
    item.save()

    return otp_code


def send_register_verification_email_notification(
    request: Request,
    user: 'AbstractBaseUser',
) -> None:
    signer = RegisterSigner({
        'user_id': get_user_verification_id(user),
    }, request=request)
    template_config_data = _get_email_template_config_data(
        request, user, NotificationType.REGISTER_VERIFICATION)

    notification_data = {
        'params_signer': signer
    }
    send_verification_notification(
        NotificationType.REGISTER_VERIFICATION, user,
        notification_data, template_config_data)


def send_register_email_verification_email_notification(
    request: Request,
    user: 'AbstractBaseUser',
    email: str,
    email_already_used: bool = False,
) -> None:
    otp_check_obj = OTPChecking()
    otp_check_obj.user = user
    otp_check_obj.notification_type_otp = NotificationTypeOTP.VERIFY_REGISTER_EMAIL.value
    otp_obj = otp_check_obj.get_otp_object({}, limit_otp_code=10)
    if otp_obj:
        otp_check_obj.check_next_otp_code_getting(otp_obj, {})

    signer = RegisterEmailSigner({
        'user_id': get_user_verification_id(user),
        'email': email,
    }, request=request)

    otp_code = make_otp_code_notification(user, NotificationTypeOTP.VERIFY_REGISTER_EMAIL)

    notification_data = {
        'params_signer': signer,
        'email_already_used': email_already_used,
        'otp_code': otp_code,
        'otp_code_time': settings.OTP_CODE_TIME_MINUTES
    }
    template_config_data = _get_email_template_config_data(
        request, user, NotificationType.REGISTER_EMAIL_VERIFICATION)
    send_verification_notification(
        NotificationType.REGISTER_EMAIL_VERIFICATION, user,
        notification_data, template_config_data, custom_user_address=email)


def send_reset_password_verification_email_notification(
    request: Request,
    user: 'AbstractBaseUser',
) -> None:
    signer = ResetPasswordSigner({
        'user_id': get_user_verification_id(user),
    }, request=request)

    # otp_check_obj = OTPChecking()
    # otp_check_obj.user = user
    # otp_check_obj.notification_type_otp = NotificationTypeOTP.VERIFY_RESET_PASSWORD.value
    # otp_obj = otp_check_obj.get_otp_object({}, limit_otp_code=5)
    # if otp_obj:
    #     otp_check_obj.check_next_otp_code_getting(otp_obj, {})

    template_config_data = _get_email_template_config_data(
        request, user, NotificationType.RESET_PASSWORD_VERIFICATION)

    otp_code = make_otp_code_notification(user, NotificationTypeOTP.VERIFY_RESET_PASSWORD)

    notification_data = {
        'params_signer': signer,
        'otp_code': otp_code,
        'otp_code_time': settings.OTP_CODE_TIME_MINUTES
    }
    send_verification_notification(
        NotificationType.RESET_PASSWORD_VERIFICATION, user, notification_data,
        template_config_data)
