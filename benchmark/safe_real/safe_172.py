# source: PyPikaSafe / pypika/queries.py
# function: get_sql

class Column:
    def get_sql(self, **kwargs: Any) -> str:
        column_sql = "{name}{type}{nullable}{default}".format(
            name=self.get_name_sql(**kwargs),
            type=" {}".format(self.type) if self.type else "",
            nullable=" {}".format("NULL" if self.nullable else "NOT NULL") if self.nullable is not None else "",
            default=" {}".format("DEFAULT " + self.default.get_sql(**kwargs)) if self.default else "",
        )

        return column_sql