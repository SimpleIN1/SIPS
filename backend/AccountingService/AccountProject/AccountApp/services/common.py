from enum import Enum


class NotificationTypeOTP(Enum):
    VERIFY_REGISTER = 1
    VERIFY_REGISTER_EMAIL = 2
    VERIFY_RESET_PASSWORD = 3
