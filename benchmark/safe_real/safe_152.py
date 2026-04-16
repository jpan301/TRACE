# source: PyPikaSafe / pypika/queries.py
# function: _force_index_sql

class QueryBuilder:
    def _force_index_sql(self, **kwargs: Any) -> str:
        return " FORCE INDEX ({indexes})".format(
            indexes=",".join(index.get_sql(**kwargs) for index in self._force_indexes),
        )