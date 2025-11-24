from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserModel(AbstractUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    username = models.CharField(verbose_name=_('Username'), max_length=150, default='', blank=True,)
    email = models.EmailField(unique=True)
    middle_name = models.CharField(max_length=150, null=True, blank=True, verbose_name="middle_name")
