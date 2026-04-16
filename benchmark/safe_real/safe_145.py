# source: DjangoSafe / django/db/backends/sqlite3/_functions.py
# function: _sqlite_datetime_extract

def _sqlite_datetime_extract(lookup_type, dt, tzname=None, conn_tzname=None):
    dt = _sqlite_datetime_parse(dt, tzname, conn_tzname)
    if dt is None:
        return None
    if lookup_type == "week_day":
        return (dt.isoweekday() % 7) + 1
    elif lookup_type == "iso_week_day":
        return dt.isoweekday()
    elif lookup_type == "week":
        return dt.isocalendar().week
    elif lookup_type == "quarter":
        return ceil(dt.month / 3)
    elif lookup_type == "iso_year":
        return dt.isocalendar().year
    else:
        return getattr(dt, lookup_type)