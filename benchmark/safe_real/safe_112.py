# source: PyPikaSafe / pypika/queries.py
# function: _body_sql

class CreateQueryBuilder:
    def _body_sql(self, **kwargs) -> str:
        clauses = self._column_clauses(**kwargs)
        clauses += self._period_for_clauses(**kwargs)
        clauses += self._unique_key_clauses(**kwargs)

        if self._primary_key:
            clauses.append(self._primary_key_clause(**kwargs))
        if self._foreign_key:
            clauses.append(self._foreign_key_clause(**kwargs))

        return ",".join(clauses)