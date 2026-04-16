# source: PyPikaSafe / pypika/terms.py
# function: _orderby_field

class AnalyticFunction:
    def _orderby_field(self, field: Field, orient: Order | None, **kwargs: Any) -> str:
        if orient is None:
            return field.get_sql(**kwargs)

        return "{field} {orient}".format(
            field=field.get_sql(**kwargs),
            orient=orient.value,
        )