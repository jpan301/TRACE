# source: PyPikaSafe / pypika/queries.py
# function: _distinct_sql

class QueryBuilder:
    def _distinct_sql(self, **kwargs: Any) -> str:
        distinct = 'DISTINCT ' if self._distinct else ''

        return distinct