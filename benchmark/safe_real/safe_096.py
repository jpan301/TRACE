# source: SentrySafe / src/sentry/api/helpers/error_upsampling.py
# function: transform_orderby_for_error_upsampling

def transform_orderby_for_error_upsampling(orderby: list[str]) -> list[str]:
    """
    Transform orderby fields to use upsampled aggregation functions instead of raw ones
    for error upsampling.

    Args:
        orderby: List of orderby strings like ["-count", "eps"]

    Returns:
        List of transformed orderby strings like ["-upsampled_count", "upsampled_eps"]
    """
    orderby_conversions = {
        "count": "upsampled_count",
        "eps": "upsampled_eps",
        "epm": "upsampled_epm",
        "sample_count": "count",
        "sample_eps": "eps",
        "sample_epm": "epm",
    }

    transformed_orderby = []
    for order_field in orderby:
        if order_field.startswith("-"):
            direction = "-"
            field = order_field[1:]
        else:
            direction = ""
            field = order_field

        # Apply transformation if field needs it
        if field in orderby_conversions:
            field = orderby_conversions[field]

        transformed_orderby.append(f"{direction}{field}")

    return transformed_orderby