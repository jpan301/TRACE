# source: SentrySafe / src/sentry/snuba/metrics/extraction.py
# function: _filter

class SearchQueryConverter:
    def _filter(self, token: SearchFilter) -> RuleCondition:
        operator = _SEARCH_TO_RELAY_OPERATORS.get(token.operator)
        if not operator:
            raise ValueError(f"Unsupported operator {token.operator}")

        # We propagate the filter in order to give as output a better error message with more context.
        key: str = token.key.name
        value: Any = token.value.raw_value
        if operator == "eq" and token.value.is_wildcard():
            condition: RuleCondition = {
                "op": "glob",
                "name": self._field_mapper(key),
                "value": [_escape_wildcard(value)],
            }
        else:
            # Special case for the `has` and `!has` operators which are parsed as follows:
            # - `has:x` -> `x != ""`
            # - `!has:x` -> `x = ""`
            # They both need to be translated to `x not eq null` and `x eq null`.
            if token.operator in ("!=", "=") and value == "":
                value = None

            if isinstance(value, str):
                value = event_search.translate_escape_sequences(value)

            condition = cast(
                RuleCondition,
                {
                    "op": operator,
                    "name": self._field_mapper(key),
                    "value": value,
                },
            )

        # In case we have negation operators, we have to wrap them in the `not` condition.
        if token.operator in ("!=", "NOT IN"):
            condition = {"op": "not", "inner": condition}

        return condition