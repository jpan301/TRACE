# source: PyPikaSafe / pypika/clickhouse/search_string.py
# function: get_sql

class _AbstractMultiSearchString:
    def get_sql(self, with_alias=False, with_namespace=False, quote_char=None, dialect=None, **kwargs):
        args = []
        for p in self.args:
            if hasattr(p, "get_sql"):
                args.append('toString("{arg}")'.format(arg=p.get_sql(with_alias=False, **kwargs)))
            else:
                args.append(str(p))

        sql = "{name}({args},[{patterns}])".format(
            name=self.name,
            args=",".join(args),
            patterns=",".join(["'%s'" % i for i in self._patterns]),
        )
        return format_alias_sql(sql, self.alias, **kwargs)