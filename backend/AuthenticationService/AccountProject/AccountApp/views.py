from datetime import datetime, timezone, timedelta

from django.db.models import Q
from django.conf import settings
from django.utils import timezone

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_registration.api.views.base import BaseAPIView
from rest_framework.response import Response
from rest_framework import status, permissions, exceptions

from rest_registration.settings import registration_settings
from rest_registration.exceptions import BadRequest, UserNotFound
from rest_registration.utils.users import get_user_verification_id
from rest_registration.signers.reset_password import ResetPasswordSigner
from rest_registration.signers.register_email import RegisterEmailSigner
from rest_registration.utils.users import (
    get_user_by_verification_id,
    get_user_email_field_name,
    is_user_email_field_unique,
    user_with_email_exists,
)

from AccountApp.exceptions import BadRequestError
from AccountApp.models import UserModel, OTPUserModel
from AccountApp.serializers import VerifyOPTEmailRegistrationSerializer, RepeatOTPCodeEmailRegistrationSerializer, \
    RepeatOTPCodeResetPasswordSerializer, VerifyOPTResetPasswordSerializer, \
    DefaultErrorSerializer, DefaultResponseSerializer, VerifyOTPEmailRegistrationResponseSerializer, \
    VerifyOTPResetPasswordResponseSerializer, DefaultRepeatErrorSerializer
from AccountApp.services.code_generator import generate_code
from AccountApp.services.common import NotificationTypeOTP
from AccountApp.services.user import get_user


class OTPChecking:
    user = None
    notification_type_otp = None

    def get_otp_object(self, data, limit_otp_code=5):

        items = OTPUserModel.objects \
                .filter(Q(user_id=self.user.id) &
                        Q(notification_type_otp=self.notification_type_otp) &
                        Q(created_at__date=datetime.now().date())) \
                .order_by("-expires")

        if len(items) >= limit_otp_code:
            raise BadRequest(detail="Limited number of code request attempts")

        return items.first() if items else None

    @staticmethod
    def confirm_otp_object(item: OTPUserModel):
        item.confirm = True
        item.save()

    @staticmethod
    def check_otp_object(item: OTPUserModel):
        if not item:
            raise BadRequest(detail={"detail": "The activation code is not found"})

    @staticmethod
    def check_otp_object_confirm(item: OTPUserModel, data):
        if item.confirm:
            raise BadRequest(detail={"detail": "The activation code has already been confirmed"},)

    @staticmethod
    def check_otp_object_expire(item: OTPUserModel, data):
        current_datetime_client = datetime.now(tz=timezone.utc)
        if item.is_expire(current_datetime_client):
            raise BadRequest(detail={"detail": "The activation code has expired"})

    @staticmethod
    def check_otp_object_equal(item: OTPUserModel, data):
        if not item.otp_code == data["otp_code"]:
            raise BadRequest(detail={"detail": "The activation code is invalid"})

    @staticmethod
    def check_next_otp_code_getting(item: OTPUserModel, data):
        current_datetime_client = datetime.now(tz=timezone.utc)
        if not item.is_get_next_code(current_datetime_client):
            time_left = str(item.next_code_time - current_datetime_client).split('.')[0]
            raise BadRequest(detail={"detail": f"You need to wait {time_left} to enter a new activation code.",
                                     "time_left": time_left})


class DefaultAPIView(BaseAPIView, OTPChecking):
    serializer_class = None
    notification_type_otp = None
    success_response_data = None
    checks = None
    user = None
    response_serializer = DefaultResponseSerializer
    error_serializer = DefaultErrorSerializer

    def find_user(self, data):
        user = get_user(id=data["user_id"])
        return user

    def _find_user_with_auth(self, data):
        if self.request.user.is_authenticated:
            user = self.request.user
        else:
            user = self.find_user(data)
            if not user:
                raise UserNotFound("User not found")
        return user

    def handle_signer(self, data) -> dict:
        pass

    def handle_notification(self, data):
        pass

    @swagger_auto_schema(
        responses={
            200: response_serializer(),
            400: openapi.Response('Bad Request', schema=error_serializer)
        }
    )
    def post(self, request):
        response_data = self.success_response_data
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        self.user = self._find_user_with_auth(data)

        item = self.get_otp_object(data)

        self.check_otp_object(item)

        for check_item in self.checks:
            if hasattr(self, check_item):
                getattr(self, check_item)(item, data)

        self.confirm_otp_object(item)

        signer_data = None
        if "handle_signer" in self.__class__.__dict__:
            signer_data = self.handle_signer(data)

        if "handle_notification" in self.__class__.__dict__:
            self.handle_notification(data)

        if signer_data:
            response_data.update(signer_data)

        return Response(
            response_data,
            status=status.HTTP_200_OK
        )


class VerifyOTPResetPasswordAPIView(DefaultAPIView):
    """
    Verify OTP code that sent by email for reset password
    """

    serializer_class = VerifyOPTResetPasswordSerializer
    notification_type_otp = NotificationTypeOTP.VERIFY_RESET_PASSWORD.value
    checks = ("check_otp_object_confirm", "check_otp_object_expire", "check_otp_object_equal",)
    success_response_data = {"detail": "The activation code is confirmed"}

    def find_user(self, data):
        user = get_user(email=data["email"])
        return user

    def handle_signer(self, data) -> dict:
        user = self.user
        signer = ResetPasswordSigner({
            'user_id': get_user_verification_id(user),
        }, request=self.request)
        return signer.get_signed_data()

    @swagger_auto_schema(
        responses={
            200: VerifyOTPResetPasswordResponseSerializer(),
            400: openapi.Response('Bad Request', schema=DefaultErrorSerializer)
        }
    )
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)


class RepeatOTPCodeResetPasswordAPIView(DefaultAPIView):
    """
    Repeat sending the OTP code for reset password
    """

    serializer_class = RepeatOTPCodeResetPasswordSerializer
    notification_type_otp = NotificationTypeOTP.VERIFY_RESET_PASSWORD.value
    checks = ("check_otp_object_confirm", "check_next_otp_code_getting", )
    success_response_data = {"detail": "Reset code sent"}

    def find_user(self, data):
        user = get_user(email=data["email"])
        return user

    def handle_notification(self, data):
        user = self.user
        if not settings.TEST:
            email_sender = registration_settings.RESET_PASSWORD_VERIFICATION_EMAIL_SENDER
            email_sender(self.request, user)

    @swagger_auto_schema(
        responses={
            200: DefaultResponseSerializer(),
            400: openapi.Response('Bad Request', schema=DefaultRepeatErrorSerializer)
        }
    )
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)


class VerifyOTPEmailRegistrationAPIView(DefaultAPIView):
    """
    Verify OTP code that sent by email
    """

    serializer_class = VerifyOPTEmailRegistrationSerializer
    notification_type_otp = NotificationTypeOTP.VERIFY_REGISTER_EMAIL.value
    checks = ("check_otp_object_confirm", "check_otp_object_expire", "check_otp_object_equal", )
    success_response_data = {"detail": "The activation code is confirmed"}
    permission_classes = [permissions.IsAuthenticated]

    def handle_signer(self, data) -> dict:
        user = self.user
        signer = RegisterEmailSigner({
            'user_id': get_user_verification_id(user),
            'email': data["email"],
        }, request=self.request)
        return signer.get_signed_data()

    @swagger_auto_schema(
        responses={
            200: VerifyOTPEmailRegistrationResponseSerializer(),
            400: openapi.Response('Bad Request', schema=DefaultErrorSerializer)
        }
    )
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)


class RepeatOTPCodeEmailRegistrationAPIView(DefaultAPIView):
    """
    Repeat sending the OTP code for registration by email
    """

    serializer_class = RepeatOTPCodeEmailRegistrationSerializer
    notification_type_otp = NotificationTypeOTP.VERIFY_REGISTER_EMAIL.value
    checks = ("check_otp_object_confirm",  "check_next_otp_code_getting", )
    success_response_data = {"detail": "Register email code email sent"}
    permission_classes = [permissions.IsAuthenticated]

    def handle_notification(self, data):
        email = data["email"]
        email_already_used = (
            is_user_email_field_unique()
            and user_with_email_exists(email))

        if not settings.TEST and registration_settings.REGISTER_EMAIL_VERIFICATION_ENABLED:
            user = self.user
            email_sender = registration_settings.REGISTER_EMAIL_VERIFICATION_EMAIL_SENDER
            email_sender(self.request, user, email, email_already_used=email_already_used)

    @swagger_auto_schema(
        responses={
            200: DefaultResponseSerializer(),
            400: openapi.Response('Bad Request', schema=DefaultRepeatErrorSerializer)
        }
    )
    def post(self, *args, **kwargs):
        return super().post(*args, **kwargs)
