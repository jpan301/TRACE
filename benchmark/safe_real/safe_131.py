# source: PyPikaSafe / pypika/terms.py
# function: get_function_sql

class AnalyticFunction:
    def get_function_sql(self, **kwargs: Any) -> str:
        function_sql = super().get_function_sql(**kwargs)
        partition_sql = self.get_partition_sql(**kwargs)

        sql = function_sql
        if self._include_over:
            sql += f" OVER({partition_sql})"

        return sql