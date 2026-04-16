# source: SentrySafe / src/sentry/snuba/metrics/extraction.py
# function: _parse_arguments

class OnDemandMetricSpec:
    def _parse_arguments(
        op: MetricOperationType, metric_type: str, parsed_field: FieldParsingResult
    ) -> Sequence[str] | None:
        requires_arguments = metric_type in ["s", "d"] or op in _MULTIPLE_ARGS_METRICS
        if not requires_arguments:
            return None

        if len(parsed_field.arguments) == 0:
            raise OnDemandMetricSpecError(f"The operation {op} supports one or more parameters")

        arguments = parsed_field.arguments
        return [_map_field_name(arguments[0])] if op not in _MULTIPLE_ARGS_METRICS else arguments