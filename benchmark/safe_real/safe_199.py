# source: PyPikaSafe / pypika/queries.py
# function: _set_sql

class QueryBuilder:
    def _set_sql(self, **kwargs: Any) -> str:
        return " SET {set}".format(
            set=",".join(
                "{field}={value}".format(
                    field=field.get_sql(**dict(kwargs, with_namespace=False)), value=value.get_sql(**kwargs)
                )
                for field, value in self._updates
            )
        )