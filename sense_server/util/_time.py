import datetime
import pytz
from sense_server.settings import TIMEZONE

TZ = pytz.timezone(TIMEZONE)


def datetime_to_seconds(dt):
    if dt is None:
        return 0
    if not dt.tzinfo:
        dt = TZ.localize(dt)
    return int((dt - datetime.datetime(1970, 1, 1, tzinfo=pytz.utc)).total_seconds())


def timestamp_to_iso_format(utc_ts, tz='UTC'):
    dt = datetime.datetime.fromtimestamp(int(utc_ts), pytz.timezone(tz))
    return dt.isoformat()


def datetime_to_iso_format(dt):
    dt.replace(tzinfo=TZ)
    return timestamp_to_iso_format(datetime_to_seconds(dt))
