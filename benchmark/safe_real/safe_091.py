# source: SentrySafe / src/sentry/search/events/fields.py
# function: resolve_datetime64

def resolve_datetime64(
    raw_value: datetime | str | float | None, precision: int = 6
) -> Function | None:
    """
    This is normally handled by the snuba-sdk but it assumes that the underlying
    table uses DateTime. Because we use DateTime64(6) as the underlying column,
    we need to cast to the same type or we risk truncating the timestamp which
    can lead to subtle errors.

    raw_value - Can be one of several types
        - None: Resolves to `None`
        - float: Assumed to be a epoch timestamp in seconds with fractional parts
        - str: Assumed to be isoformat timestamp in UTC time (without timezone info)
        - datetime: Will be formatted as a isoformat timestamp in UTC time
    """

    value: str | float | None = None

    if isinstance(raw_value, datetime):
        if raw_value.tzinfo is not None:
            # This is adapted from snuba-sdk
            # See https://github.com/getsentry/snuba-sdk/blob/2f7f014920b4f527a87f18c05b6aa818212bec6e/snuba_sdk/visitors.py#L168-L172
            delta = raw_value.utcoffset()
            assert delta is not None
            raw_value -= delta
            raw_value = raw_value.replace(tzinfo=None)
        value = raw_value.isoformat()
    elif isinstance(raw_value, float):
        value = raw_value

    if value is None:
        return None

    return Function("toDateTime64", [value, precision])