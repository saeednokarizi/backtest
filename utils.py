import datetime
import pytz



def ms_to_dt(ms: int) -> datetime.datetime:
    utc_dt = datetime.datetime.utcfromtimestamp(ms / 1000)
    tehran_tz = pytz.timezone('Asia/Tehran')
    tehran_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(tehran_tz)
    return tehran_dt