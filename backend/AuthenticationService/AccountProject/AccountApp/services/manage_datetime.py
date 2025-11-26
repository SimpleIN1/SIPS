from datetime import datetime, timezone, timedelta


def is_expiration_time(datetime_created: str, minutes: int):
    """
    Проверяет, что не истекло сколько-то минут (e.g. datetime_created = 1763219817)
    :param datetime_created:
    :param minutes:
    :return:
    """

    datetime_created = int(datetime_created)
    return ((datetime.now(timezone.utc) -
             datetime.fromtimestamp(datetime_created, timezone.utc)) <
            timedelta(minutes=minutes))
