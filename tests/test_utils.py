from datetime import timezone

from lxd.utils import parse_datetime_with_nanoseconds


def test_parse_datetime_with_nanoseconds():
    value = parse_datetime_with_nanoseconds('2022-07-08T15:34:06.762246839Z')
    assert value.year == 2022
    assert value.month == 7
    assert value.day == 8
    assert value.hour == 15
    assert value.minute == 34
    assert value.second == 6
    assert value.microsecond == 762246
    assert value.tzinfo == timezone.utc
