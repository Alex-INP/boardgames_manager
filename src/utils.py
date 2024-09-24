from datetime import datetime

import pytz
from dateutil.relativedelta import relativedelta


def get_now_utc() -> datetime:
    return datetime.now(pytz.timezone("UTC"))


def get_past_utc(**kwargs) -> datetime:
    return get_now_utc() - relativedelta(**kwargs)


def get_future_utc(**kwargs) -> datetime:
    return get_now_utc() + relativedelta(**kwargs)


def get_as_utc(value: datetime) -> datetime:
    if not value.tzinfo:
        return pytz.UTC.localize(value)
    return value.astimezone(pytz.timezone("UTC"))


def get_as_msk(value: datetime) -> datetime:
    if not value.tzinfo:
        return pytz.timezone("Europe/Moscow").localize(value)
    return value.astimezone(pytz.timezone("Europe/Moscow"))
