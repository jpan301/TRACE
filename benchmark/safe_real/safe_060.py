# source: PyPikaSafe / pypika/dialects.py
# function: get_sql

class MSSQLQueryBuilder:
    def get_sql(self, *args: Any, **kwargs: Any) -> str:
        # MSSQL does not support group by a field alias.
        # Note: set directly in kwargs as they are re-used down the tree in the case of subqueries!
        kwargs['groupby_alias'] = False
        return super().get_sql(*args, **kwargs)