from datetime import datetime

from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, UserManager


class UserManagerCustom(UserManager):
    def create_user(self, username=None, email=None, password=None, **extra_fields):
        username = email.split("@")[0]
        return super().create_user(username, email, password, **extra_fields)


class UserModel(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    username = models.CharField(verbose_name=_('Username'), max_length=150, default='', blank=True,)
    email = models.EmailField(unique=True)
    middle_name = models.CharField(max_length=150, null=True, blank=True, verbose_name="middle_name")
    organization_name = models.CharField(max_length=150, null=True, blank=True, verbose_name="organization_name")

    objects = UserManagerCustom()

    class Meta:
        db_table = "auth_user"


class OTPUserModel(models.Model):
    NOTIFICATION_TYPE_OTP_CHOICES = (
        (0, "Default"),
        (1, "Verify register"),
        (2, "Verify register email"),
        (3, "Verify reset password"),
    )

    user = models.ForeignKey("AccountApp.UserModel", on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6, validators=[MinLengthValidator(6)])
    expires = models.DateTimeField()
    next_code_time = models.DateTimeField(null=True, blank=True)
    confirm = models.BooleanField(default=False)
    notification_type_otp = models.SmallIntegerField(choices=NOTIFICATION_TYPE_OTP_CHOICES, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expire(self, current_client_time: datetime):
        return current_client_time > self.expires

    def is_get_next_code(self, current_client_time: datetime):
        return current_client_time > self.next_code_time

    def __str__(self):
        return f"OTPUserModel(opt_code={self.otp_code})"

    class Meta:
        db_table = "otp_user"
