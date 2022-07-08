from datetime import datetime, timezone
from functools import lru_cache


@lru_cache(32)
def parse_datetime(value: str) -> datetime:
    return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')


def parse_datetime_with_nanoseconds(value: str) -> datetime:
    dt, nanoseconds = value.rsplit('.', 1)
    obj = parse_datetime(dt)
    return obj.replace(microsecond=int(nanoseconds[:6]), tzinfo=timezone.utc)
