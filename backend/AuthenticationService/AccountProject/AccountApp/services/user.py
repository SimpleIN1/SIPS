from __future__ import annotations

from AccountApp.models import UserModel


def get_user(**kwargs) -> UserModel | None:
    try:
        return UserModel.objects.get(**kwargs)
    except UserModel.DoesNotExist:
        return None