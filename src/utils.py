from datetime import datetime

import pytz


def get_now_utc() -> datetime:
    return datetime.now(pytz.timezone("UTC"))


def get_as_utc(value: datetime) -> datetime:
    if not value.tzinfo:
        return pytz.UTC.localize(value)
    return value.astimezone(pytz.timezone("UTC"))


def get_as_msk(value: datetime) -> datetime:
    if not value.tzinfo:
        return pytz.timezone("Europe/Moscow").localize(value)
    return value.astimezone(pytz.timezone("Europe/Moscow"))
