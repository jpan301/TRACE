# source: DjangoSafe / django/utils/feedgenerator.py
# function: rfc3339_date

def rfc3339_date(date):
    if not isinstance(date, datetime.datetime):
        date = datetime.datetime.combine(date, datetime.time())
    return date.isoformat() + ("Z" if date.utcoffset() is None else "")