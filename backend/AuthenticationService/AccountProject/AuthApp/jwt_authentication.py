from typing import TypeVar

from django.contrib.auth.models import AbstractBaseUser
from rest_framework_simplejwt.models import TokenUser
from rest_framework_simplejwt.settings import api_settings


AuthUser = TypeVar("AuthUser", AbstractBaseUser, TokenUser)


def default_user_authentication_rule(user: AuthUser) -> bool:
    return user is not None and (
        not api_settings.CHECK_USER_IS_ACTIVE or user.is_active
    ) and user.is_verify
