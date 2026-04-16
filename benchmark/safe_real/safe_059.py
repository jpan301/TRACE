# source: PyPikaSafe / pypika/dialects.py
# function: _apply_pagination

class MSSQLQueryBuilder:
    def _apply_pagination(self, querystring: str, **kwargs) -> str:
        # Note: Overridden as MSSQL specifies offset before the fetch next limit
        if self._limit is not None or self._offset:
            # Offset has to be present if fetch next is specified in a MSSQL query
            querystring += self._offset_sql()

        if self._limit is not None:
            querystring += self._limit_sql()

        return querystring