import time
from datetime import datetime, UTC


def get_unix_time():
    date_time = datetime.now(UTC)
    return time.mktime(date_time.timetuple())
