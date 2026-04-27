import time
from datetime import datetime, timedelta, timezone

from django.db.models import Q
from django.conf import settings
from django.urls import reverse_lazy
from django.test import TestCase, Client, RequestFactory

from AccountApp.models import UserModel, OTPUserModel
from AccountApp.services.common import NotificationTypeOTP
from AccountApp.services.code_generator import generate_code


VERIFY_REGISTRATION_URL_NAME = "verify-registration"
VERIFY_OTPCODE_EMAIL_REGISTRATION_URL_NAME = "verify-otpcode-email"
VERIFY_EMAIL_REGISTRATION_URL_NAME = "verify-change-email"
VERIFY_OTPCODE_RESET_PASSWORD_URL_NAME = "verify-otpcode-reset-password"

REPEAT_CODE_REGISTRATION_URL_NAME = "repeat-otpcode-registration"
REPEAT_OTPCODE_EMAIL_REGISTRATION_URL_NAME = "repeat-otpcode-email"
REPEAT_OTPCODE_RESET_PASSWORD_URL_NAME = "repeat-otpcode-reset-password"

TOKEN_OBTAIN_PAIR = "token_obtain_pair"


class VerifyRegisterTestCase:
    def test_verify_register(self):

        user = UserModel.objects.create_user(
            "user", "user@mail.ru", "asd_asdf#sdf-daDD"
        )
        datetime_now = datetime.now(tz=timezone.utc)
        OTPUserModel.objects.create(
            user=user, otp_code="123123",
            expires=datetime_now + timedelta(minutes=settings.OTP_CODE_TIME_MINUTES),
            next_code_time=datetime_now + timedelta(minutes=1),
            notification_type_otp=NotificationTypeOTP.VERIFY_REGISTER.value
        )
        OTPUserModel.objects.create(
            user=user, otp_code="123124",
            expires=datetime_now + timedelta(minutes=1) + timedelta(minutes=settings.OTP_CODE_TIME_MINUTES),
            next_code_time=datetime_now + timedelta(minutes=2),
            notification_type_otp=NotificationTypeOTP.VERIFY_RESET_PASSWORD.value
        )
        OTPUserModel.objects.create(
            user=user, otp_code="123125",
            expires=datetime_now + timedelta(minutes=1) + timedelta(minutes=settings.OTP_CODE_TIME_MINUTES),
            next_code_time=datetime_now + timedelta(minutes=2),
            notification_type_otp=NotificationTypeOTP.VERIFY_REGISTER.value
        )

        data = {
            "user_id": user.id,
            "otp_code": "123125",
            "timestamp": int(time.time())
        }
        response = self.client.post(reverse_lazy(VERIFY_REGISTRATION_URL_NAME), data=data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, {"detail": "User verified successfully"},)

    def test_verify_is_confirm_register(self):
        user = UserModel.objects.create_user(
            "user", "user@mail.ru", "asd_asdf#sdf-daDD"
        )
        otp_code = "123123"
        datetime_now = datetime.now(tz=timezone.utc)
        OTPUserModel.objects.create(
            user=user, otp_code=otp_code,
            expires=datetime_now + timedelta(minutes=settings.OTP_CODE_TIME_MINUTES),
            next_code_time=datetime_now + timedelta(minutes=1),
            notification_type_otp=NotificationTypeOTP.VERIFY_REGISTER.value,
            confirm=True,
        )
        data = {
            "user_id": user.id,
            "otp_code": otp_code,
            "timestamp": int((datetime.now() + timedelta(minutes=1, seconds=15)).timestamp())
        }
        response = self.client.post(reverse_lazy(VERIFY_REGISTRATION_URL_NAME), data=data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"detail": "The activation code has already been confirmed"})

    def test_verify_code_not_found_register(self):
        user = UserModel.objects.create_user(
            "user", "user@mail.ru", "asd_asdf#sdf-daDD"
        )
        otp_code = "123123"
        datetime_now = datetime.now(tz=timezone.utc)
        OTPUserModel.objects.create(
            user=user, otp_code=otp_code,
            expires=datetime_now + timedelta(minutes=settings.OTP_CODE_TIME_MINUTES),
            next_code_time=datetime_now + timedelta(minutes=1),
            notification_type_otp=NotificationTypeOTP.VERIFY_REGISTER.value,
            confirm=True,
        )
        data = {
            "user_id": 20,
            "otp_code": otp_code,
            "timestamp": int((datetime.now() + timedelta(minutes=1, seconds=15)).timestamp())
        }
        response = self.client.post(reverse_lazy(VERIFY_REGISTRATION_URL_NAME), data=data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"detail": "The activation code is not found"})


class RepeatCodeRegisterTestCase:
    def test_repeat_code_time_left_register(self):
        user = UserModel.objects.create_user(
            "user", "user@mail.ru", "asd_asdf#sdf-daDD"
        )
        datetime_now = datetime.now(tz=timezone.utc)
        OTPUserModel.objects.create(
            user=user, otp_code="123123",
            expires=datetime_now + timedelta(minutes=settings.OTP_CODE_TIME_MINUTES),
            next_code_time=datetime_now + timedelta(minutes=1),
            notification_type_otp=NotificationTypeOTP.VERIFY_REGISTER.value
        )
        data = {
            "user_id": user.id,
            "timestamp": int((datetime.now() + timedelta(seconds=15)).timestamp())
        }
        response = self.client.post(reverse_lazy(REPEAT_CODE_REGISTRATION_URL_NAME), data=data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'detail': 'You need to wait 0:00:45 to enter a new activation code.'})

    def test_repeat_code_register(self):
        user = UserModel.objects.create_user(
            "user", "user@mail.ru", "asd_asdf#sdf-daDD"
        )
        datetime_now = datetime.now(tz=timezone.utc)
        OTPUserModel.objects.create(
            user=user, otp_code="123123",
            expires=datetime_now + timedelta(minutes=settings.OTP_CODE_TIME_MINUTES),
            next_code_time=datetime_now + timedelta(minutes=1),
            notification_type_otp=NotificationTypeOTP.VERIFY_REGISTER.value
        )
        data = {
            "user_id": user.id,
            "timestamp": int((datetime.now() + timedelta(minutes=1, seconds=15)).timestamp())
        }
        response = self.client.post(reverse_lazy(REPEAT_CODE_REGISTRATION_URL_NAME), data=data)

        self.assertEqual(response.status_code, 200)

        detail = "The activation code has been successfully sent to the mail"
        self.assertEqual(response.data.get("detail"), detail)

    def test_repeat_code_is_confirm_register(self):
        user = UserModel.objects.create_user(
            "user", "user@mail.ru", "asd_asdf#sdf-daDD"
        )
        datetime_now = datetime.now(tz=timezone.utc)
        OTPUserModel.objects.create(
            user=user, otp_code="123123",
            expires=datetime_now + timedelta(minutes=settings.OTP_CODE_TIME_MINUTES),
            next_code_time=datetime_now + timedelta(minutes=1),
            notification_type_otp=NotificationTypeOTP.VERIFY_REGISTER.value,
            confirm=True,
        )
        data = {
            "user_id": user.id,
            "timestamp": int((datetime.now() + timedelta(minutes=1, seconds=15)).timestamp())
        }
        response = self.client.post(reverse_lazy(REPEAT_CODE_REGISTRATION_URL_NAME), data=data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"detail": "The activation code has already been confirmed"})

    def test_repeat_code_not_found_register(self):
        user = UserModel.objects.create_user(
            "user", "user@mail.ru", "asd_asdf#sdf-daDD"
        )
        otp_code = "123123"
        datetime_now = datetime.now(tz=timezone.utc)
        OTPUserModel.objects.create(
            user=user, otp_code=otp_code,
            expires=datetime_now + timedelta(minutes=settings.OTP_CODE_TIME_MINUTES),
            next_code_time=datetime_now + timedelta(minutes=1),
            notification_type_otp=NotificationTypeOTP.VERIFY_REGISTER.value,
            confirm=True,
        )
        data = {
            "user_id": 20,
            "otp_code": otp_code,
            "timestamp": int((datetime.now() + timedelta(minutes=1, seconds=15)).timestamp())
        }
        response = self.client.post(reverse_lazy(REPEAT_CODE_REGISTRATION_URL_NAME), data=data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {"detail": "The activation code is not found"})


class VerifyOTPEmailRegistrationTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "user",
            "email": "user@mail.ru",
            "password": "asd_asdf#sdf-daDD",
        }
        self.user = UserModel.objects.create_user(**self.user_data)

    def get_access_token(self):

        data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(reverse_lazy(TOKEN_OBTAIN_PAIR), data=data)
        self.assertEqual(response.status_code, 200)
        return response.data["access"]

    def test_verify_otp_email_registration(self):
        otp_code = "123123"
        datetime_now = datetime.now(tz=timezone.utc)
        OTPUserModel.objects.create(
            user=self.user, otp_code=otp_code,
            expires=datetime_now + timedelta(minutes=settings.OTP_CODE_TIME_MINUTES),
            next_code_time=datetime_now + timedelta(minutes=1),
            notification_type_otp=NotificationTypeOTP.VERIFY_REGISTER_EMAIL.value,
        )
        data = {
            "user_id": self.user.id,
            "otp_code": otp_code,
            "email": "user@mail.ru",
        }
        headers = {
            "Authorization": f"Bearer {self.get_access_token()}"
        }
        response = self.client.post(reverse_lazy(VERIFY_OTPCODE_EMAIL_REGISTRATION_URL_NAME),
                                    data=data, headers=headers)
        self.assertEqual(response.status_code, 200)

        detail = "The activation code is confirmed"
        received_detail = response.data.pop("detail")
        keys = list(response.data.keys())
        expected_keys = ["email", "user_id", "signature", "timestamp"]
        expected_keys.extend(keys)
        expected_keys = list(set(expected_keys))

        self.assertEqual(received_detail, detail)
        self.assertEqual(len(keys), len(expected_keys))

        otp_object = OTPUserModel.objects \
            .select_related("user") \
            .filter(Q(user_id=self.user.id) &
                    Q(notification_type_otp=NotificationTypeOTP.VERIFY_REGISTER_EMAIL.value)) \
            .order_by("-expires").first()

        self.assertEqual(otp_object.otp_code, otp_code)
        self.assertEqual(otp_object.confirm, True)

    def test_verify_otp_email_registration_code_not_found(self):
        otp_code = "123123"
        data = {
            "user_id": self.user.id,
            "otp_code": otp_code,
            "email": "user@mail.ru"
        }
        headers = {
            "Authorization": f"Bearer {self.get_access_token()}"
        }
        response = self.client.post(reverse_lazy(VERIFY_OTPCODE_EMAIL_REGISTRATION_URL_NAME),
                                    data=data, headers=headers)
        self.assertEqual(response.status_code, 400)

        detail = "The activation code is not found"
        received_detail = response.data.pop("detail")

        self.assertEqual(received_detail, detail)

    def test_verify_otp_email_registration_confirmed_otp_code(self):
        otp_code = "123123"
        datetime_now = datetime.now(tz=timezone.utc)
        OTPUserModel.objects.create(
            user=self.user, otp_code=otp_code,
            expires=datetime_now + timedelta(minutes=settings.OTP_CODE_TIME_MINUTES),
            next_code_time=datetime_now + timedelta(minutes=1),
            notification_type_otp=NotificationTypeOTP.VERIFY_REGISTER_EMAIL.value,
            confirm=True,
        )
        data = {
            "user_id": self.user.id,
            "otp_code": otp_code,
            "email": "user@mail.ru"
        }
        headers = {
            "Authorization": f"Bearer {self.get_access_token()}"
        }
        response = self.client.post(reverse_lazy(VERIFY_OTPCODE_EMAIL_REGISTRATION_URL_NAME),
                                    data=data, headers=headers)

        self.assertEqual(response.status_code, 400)

        detail = "The activation code has already been confirmed"
        received_detail = response.data.pop("detail")

        self.assertEqual(received_detail, detail)

        otp_object = OTPUserModel.objects \
            .select_related("user") \
            .filter(Q(user_id=self.user.id) &
                    Q(notification_type_otp=NotificationTypeOTP.VERIFY_REGISTER_EMAIL.value)) \
            .order_by("-expires").first()

        self.assertEqual(otp_object.otp_code, otp_code)
        self.assertEqual(otp_object.confirm, True)


class RepeatOTPEmailRegistrationTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "user",
            "email": "user@mail.ru",
            "password": "asd_asdf#sdf-daDD",
        }
        self.user = UserModel.objects.create_user(**self.user_data)

    def get_access_token(self):
        data = {
            "email": self.user_data["email"],
            "password": self.user_data["password"],
        }
        response = self.client.post(reverse_lazy(TOKEN_OBTAIN_PAIR), data=data)
        self.assertEqual(response.status_code, 200)
        return response.data["access"]

    def test_repeat_otp_email_registration_time_left(self):
        otp_code = "123123"
        datetime_now = datetime.now(tz=timezone.utc)
        OTPUserModel.objects.create(
            user=self.user, otp_code=otp_code,
            expires=datetime_now + timedelta(minutes=settings.OTP_CODE_TIME_MINUTES),
            next_code_time=datetime_now + timedelta(minutes=1) - timedelta(seconds=15),
            notification_type_otp=NotificationTypeOTP.VERIFY_REGISTER_EMAIL.value,
        )
        data = {
            "email": "user@mail.ru",
        }
        headers = {
            "Authorization": f"Bearer {self.get_access_token()}"
        }
        response = self.client.post(reverse_lazy(REPEAT_OTPCODE_EMAIL_REGISTRATION_URL_NAME),
                                    data=data, headers=headers)

        self.assertEqual(response.status_code, 400)

        excepted_data = {'detail': 'You need to wait 0:00:44 to enter a new activation code.', 'time_left': '0:00:44'}
        self.assertEqual(response.data, excepted_data)

    def test_repeat_otp_email_registration(self):
        otp_code = "123123"
        datetime_now = datetime.now(tz=timezone.utc)
        OTPUserModel.objects.create(
            user=self.user, otp_code=otp_code,
            expires=datetime_now + timedelta(minutes=settings.OTP_CODE_TIME_MINUTES),
            next_code_time=datetime_now - timedelta(minutes=1, seconds=10),
            notification_type_otp=NotificationTypeOTP.VERIFY_REGISTER_EMAIL.value,
        )
        data = {
            "email": "user@mail.ru",
        }
        headers = {
            "Authorization": f"Bearer {self.get_access_token()}"
        }
        response = self.client.post(reverse_lazy(REPEAT_OTPCODE_EMAIL_REGISTRATION_URL_NAME),
                                    data=data, headers=headers)

        self.assertEqual(response.status_code, 200)
        excepted_data = {"detail": "Register email code email sent"}
        self.assertEqual(response.data, excepted_data)

    def test_repeat_otp_email_registration_limited_code(self):

        for i in range(5):
            otp_code = generate_code()
            datetime_now = datetime.now(tz=timezone.utc)
            OTPUserModel.objects.create(
                user=self.user, otp_code=otp_code,
                expires=datetime_now + timedelta(minutes=settings.OTP_CODE_TIME_MINUTES),
                next_code_time=datetime_now - timedelta(minutes=1, seconds=10),
                notification_type_otp=NotificationTypeOTP.VERIFY_REGISTER_EMAIL.value,
            )

        data = {
            "email": "user@mail.ru",
        }
        headers = {
            "Authorization": f"Bearer {self.get_access_token()}"
        }
        response = self.client.post(reverse_lazy(REPEAT_OTPCODE_EMAIL_REGISTRATION_URL_NAME),
                                    data=data, headers=headers)

        self.assertEqual(response.status_code, 400)
        excepted_data = {"detail": "Limited number of code request attempts"}
        self.assertEqual(response.data, excepted_data)


class VerifyOTPResetPasswordTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "user",
            "email": "user@mail.ru",
            "password": "asd_asdf#sdf-daDD",
        }
        self.user = UserModel.objects.create_user(**self.user_data)

    def test_verify_otp_reset_password(self):
        otp_code = "123123"
        datetime_now = datetime.now(tz=timezone.utc)
        OTPUserModel.objects.create(
            user=self.user, otp_code=otp_code,
            expires=datetime_now + timedelta(minutes=settings.OTP_CODE_TIME_MINUTES),
            next_code_time=datetime_now + timedelta(minutes=1),
            notification_type_otp=NotificationTypeOTP.VERIFY_RESET_PASSWORD.value,
        )
        data = {
            "email": self.user.email,
            "otp_code": otp_code,
        }
        response = self.client.post(reverse_lazy(VERIFY_OTPCODE_RESET_PASSWORD_URL_NAME), data=data)
        self.assertEqual(response.status_code, 200)

        detail = "The activation code is confirmed"
        received_detail = response.data.pop("detail")
        keys = list(response.data.keys())
        expected_keys = ["user_id", "signature", "timestamp"]
        expected_keys.extend(keys)
        expected_keys = list(set(expected_keys))

        self.assertEqual(received_detail, detail)
        self.assertEqual(len(keys), len(expected_keys))

        otp_object = OTPUserModel.objects \
            .select_related("user") \
            .filter(Q(user_id=self.user.id) &
                    Q(notification_type_otp=NotificationTypeOTP.VERIFY_RESET_PASSWORD.value)) \
            .order_by("-expires").first()

        self.assertEqual(otp_object.otp_code, otp_code)
        self.assertEqual(otp_object.confirm, True)


class RepeatOTPResetPasswordTestCase(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "user",
            "email": "user@mail.ru",
            "password": "asd_asdf#sdf-daDD",
        }
        self.user = UserModel.objects.create_user(**self.user_data)

    def test_repeat_otp_reset_password(self):
        otp_code = "123123"
        datetime_now = datetime.now(tz=timezone.utc)
        OTPUserModel.objects.create(
            user=self.user, otp_code=otp_code,
            expires=datetime_now + timedelta(minutes=settings.OTP_CODE_TIME_MINUTES),
            next_code_time=datetime_now - timedelta(minutes=1, seconds=10),
            notification_type_otp=NotificationTypeOTP.VERIFY_RESET_PASSWORD.value,
        )
        data = {
            "email": "user@mail.ru",
        }
        response = self.client.post(reverse_lazy(REPEAT_OTPCODE_RESET_PASSWORD_URL_NAME),
                                    data=data)

        self.assertEqual(response.status_code, 200)
        excepted_data = {"detail": "Reset code sent"}
        self.assertEqual(response.data, excepted_data)

    def test_repeat_otp_email_registration_limited_code(self):

        for i in range(5):
            otp_code = generate_code()
            datetime_now = datetime.now(tz=timezone.utc)
            OTPUserModel.objects.create(
                user=self.user, otp_code=otp_code,
                expires=datetime_now + timedelta(minutes=settings.OTP_CODE_TIME_MINUTES),
                next_code_time=datetime_now - timedelta(minutes=1, seconds=10),
                notification_type_otp=NotificationTypeOTP.VERIFY_RESET_PASSWORD.value,
            )

        data = {
            "email": "user@mail.ru",
        }
        response = self.client.post(reverse_lazy(REPEAT_OTPCODE_RESET_PASSWORD_URL_NAME), data=data)

        self.assertEqual(response.status_code, 400)
        excepted_data = {"detail": "Limited number of code request attempts"}
        self.assertEqual(response.data, excepted_data)
