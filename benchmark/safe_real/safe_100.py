# source: PyPikaSafe / pypika/clickhouse/array.py
# function: get_sql

class Array:
    def get_sql(self):
        if self._converter_cls:
            converted = []
            for value in self._values:
                converter = self._converter_cls(value, **self._converter_options)
                converted.append(converter.get_sql())
            sql = "".join(["[", ",".join(converted), "]"])

        else:
            sql = str(self._values)

        return format_alias_sql(sql, self.alias)