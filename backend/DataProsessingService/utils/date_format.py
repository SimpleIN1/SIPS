from datetime import datetime


def format_date_time(date_time: str, format: str):
    datetime_fixed = datetime.strptime(
        f"{date_time}",
        f"{format}"
    )
    return datetime_fixed
