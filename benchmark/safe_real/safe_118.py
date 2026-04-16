# source: PyPikaSafe / pypika/dialects.py
# function: top

class MSSQLQueryBuilder:
    def top(self, value: str | int, percent: bool = False, with_ties: bool = False) -> None:
        """
        Implements support for simple TOP clauses.
        https://docs.microsoft.com/en-us/sql/t-sql/queries/top-transact-sql?view=sql-server-2017
        """
        try:
            self._top = int(value)
        except ValueError:
            raise QueryException("TOP value must be an integer")

        if percent and not (0 <= int(value) <= 100):
            raise QueryException("TOP value must be between 0 and 100 when `percent`" " is specified")
        self._top_percent: bool = percent
        self._top_with_ties: bool = with_ties