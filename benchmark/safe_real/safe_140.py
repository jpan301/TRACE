# source: DjangoSafe / django/utils/duration.py
# function: duration_string

def duration_string(duration):
    """Version of str(timedelta) which is not English specific."""
    days, hours, minutes, seconds, microseconds = _get_duration_components(duration)

    string = "{:02d}:{:02d}:{:02d}".format(hours, minutes, seconds)
    if days:
        string = "{} ".format(days) + string
    if microseconds:
        string += ".{:06d}".format(microseconds)

    return string