# source: PyPikaSafe / pypika/terms.py
# function: get_sql

class ContainsCriterion:
    def get_sql(self, subquery: Any = None, **kwargs: Any) -> str:
        sql = "{term} {not_}IN {container}".format(
            term=self.term.get_sql(**kwargs),
            container=self.container.get_sql(subquery=True, **kwargs),
            not_="NOT " if self._is_negated else "",
        )
        return format_alias_sql(sql, self.alias, **kwargs)