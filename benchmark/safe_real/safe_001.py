# source: SentrySafe / src/sentry/snuba/metrics/naming_layer/mri.py
# function: format_mri_field_value

def format_mri_field_value(field: str, value: str) -> str:
    """
    Formats MRI field value to a human-readable format using unit.

    For example, if the value of avg(c:transactions/duration@second) is 60,
    it will be returned as 1 minute.

    """
    try:
        parsed_mri_field = parse_mri_field(field)
        if parsed_mri_field is None:
            return value

        return format_value_using_unit_and_op(
            float(value), parsed_mri_field.mri.unit, parsed_mri_field.op
        )

    except InvalidParams:
        return value