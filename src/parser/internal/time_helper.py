import time
from datetime import datetime
from pytz import timezone


# now() returns current timestamp in specific timezone (default is UTC)
def now(tz="utc"):
    if tz == "utc":
        return now_in_utc()

    if tz == "kg":
        tz = 'Asia/Bishkek'
    elif tz == "kz":
        tz = 'Asia/Almaty'
    else:
        tz = 'Asia/Dushanbe'

    return int(time.mktime(datetime.now(timezone(tz)).timetuple()))


# now_in_utc() returns current timestamp in UTC
def now_in_utc():
    utcnow = datetime.utcnow()
    epoch = (utcnow - datetime(1970, 1, 1)).total_seconds()
    return int(epoch)


# now_date_key() returns current time in format YYY-MM-DD for specific country (default Tajikistan)
def now_date_key(country="tj"):
    if country == "kg":
        tz = 'Asia/Bishkek'
    elif country == "kz":
        tz = 'Asia/Almaty'
    else:
        # uzbekistan on same timezone
        tz = 'Asia/Dushanbe'

    today = datetime.now(timezone(tz))
    return today.strftime("%Y-%-m-%-d")


# now_date_key_wlz() returns same date as now_date_key() but with leading zeros
def now_date_key_wlz(country="tj"):
    if country == "kg":
        tz = 'Asia/Bishkek'
    elif country == "kz":
        tz = 'Asia/Almaty'
    else:
        # uzbekistan on same timezone
        tz = 'Asia/Dushanbe'

    today = datetime.now(timezone(tz))
    return today.strftime("%Y-%m-%d")
