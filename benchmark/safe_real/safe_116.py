# source: PyPikaSafe / pypika/dialects.py
# function: _as_select_sql

class VerticaCreateQueryBuilder:
    def _as_select_sql(self, **kwargs: Any) -> str:
        return "{preserve_rows} AS ({query})".format(
            preserve_rows=self._preserve_rows_sql(),
            query=self._as_select.get_sql(**kwargs),
        )