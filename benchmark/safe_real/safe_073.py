# source: PyPikaSafe / pypika/queries.py
# function: get_sql

class JoinUsing:
    def get_sql(self, **kwargs: Any) -> str:
        join_sql = super().get_sql(**kwargs)
        return "{join} USING ({fields})".format(
            join=join_sql,
            fields=",".join(field.get_sql(**kwargs) for field in self.fields),
        )