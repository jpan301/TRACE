# source: PyPikaSafe / pypika/clickhouse/array.py
# function: get_sql

class _AbstractArrayFunction:
    def get_sql(self, with_namespace=False, quote_char=None, dialect=None, **kwargs):
        array = self._array.get_sql()
        sql = "{name}({array})".format(
            name=self.name,
            array='"%s"' % array if isinstance(self._array, Field) else array,
        )
        return format_alias_sql(sql, self.alias, **kwargs)