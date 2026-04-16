# source: PyPikaSafe / pypika/queries.py
# function: _apply_terms

class QueryBuilder:
    def _apply_terms(self, *terms: Any) -> None:
        """
        Handy function for INSERT and REPLACE statements in order to check if
        terms are introduced and how append them to `self._values`
        """
        if self._insert_table is None:
            raise AttributeError("'Query' object has no attribute '%s'" % "insert")

        if not terms:
            return

        if not isinstance(terms[0], (list, tuple, set)):
            terms = [terms]

        for values in terms:
            self._values.append([value if isinstance(value, Term) else self.wrap_constant(value) for value in values])