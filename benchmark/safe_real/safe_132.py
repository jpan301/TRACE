# source: PyPikaSafe / pypika/queries.py
# function: _select_field_str

class QueryBuilder:
    def _select_field_str(self, term: str) -> None:
        if 0 == len(self._from):
            raise QueryException(f"Cannot select {term}, no FROM table specified.")

        if term == "*":
            self._select_star = True
            self._selects = [Star()]
            return

        self._select_field(Field(term, table=self._from[0]))