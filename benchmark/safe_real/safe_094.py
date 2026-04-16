# source: PyPikaSafe / pypika/queries.py
# function: columns

class QueryBuilder:
    def columns(self, *terms: Any) -> None:
        if self._insert_table is None:
            raise AttributeError("'Query' object has no attribute '%s'" % "insert")

        if terms and isinstance(terms[0], (list, tuple)):
            terms = terms[0]

        for term in terms:
            if isinstance(term, str):
                term = Field(term, table=self._insert_table)
            self._columns.append(term)