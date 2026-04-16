# source: PyPikaSafe / pypika/dialects.py
# function: get_sql

class PostgreSQLQueryBuilder:
    def get_sql(self, with_alias: bool = False, subquery: bool = False, **kwargs: Any) -> str:
        self._set_kwargs_defaults(kwargs)

        querystring = super().get_sql(with_alias, subquery, **kwargs)

        querystring += self._on_conflict_sql(**kwargs)
        querystring += self._on_conflict_action_sql(**kwargs)

        if self._returns:
            kwargs['with_namespace'] = self._update_table and self.from_
            querystring += self._returning_sql(**kwargs)
        return querystring