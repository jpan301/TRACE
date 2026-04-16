# source: PyPikaSafe / pypika/dialects.py
# function: get_sql

class ClickHouseDropQueryBuilder:
    def get_sql(self, **kwargs: Any) -> str:
        query = super().get_sql(**kwargs)

        if self._drop_target_kind != "DICTIONARY" and self._cluster_name is not None:
            query += " ON CLUSTER " + format_quotes(self._cluster_name, super().QUOTE_CHAR)

        return query