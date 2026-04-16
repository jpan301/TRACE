# source: PyPikaSafe / pypika/queries.py
# function: get_sql

class _SetOperation:
    def get_sql(self, with_alias: bool = False, subquery: bool = False, **kwargs: Any) -> str:
        set_operation_template = " {type} {query_string}"

        kwargs.setdefault("dialect", self.base_query.dialect)
        # This initializes the quote char based on the base query, which could be a dialect specific query class
        # This might be overridden if quote_char is set explicitly in kwargs
        kwargs.setdefault("quote_char", self.base_query.QUOTE_CHAR)

        base_querystring = self.base_query.get_sql(subquery=self.base_query.wrap_set_operation_queries, **kwargs)

        querystring = base_querystring
        for set_operation, set_operation_query in self._set_operation:
            set_operation_querystring = set_operation_query.get_sql(
                subquery=self.base_query.wrap_set_operation_queries, **kwargs
            )

            if len(self.base_query._selects) != len(set_operation_query._selects):
                raise SetOperationException(
                    "Queries must have an equal number of select statements in a set operation."
                    "\n\nMain Query:\n{query1}\n\nSet Operations Query:\n{query2}".format(
                        query1=base_querystring, query2=set_operation_querystring
                    )
                )

            querystring += set_operation_template.format(
                type=set_operation.value, query_string=set_operation_querystring
            )

        if self._orderbys:
            querystring += self._orderby_sql(**kwargs)

        if self._limit is not None:
            querystring += self._limit_sql()

        if self._offset:
            querystring += self._offset_sql()

        if subquery:
            querystring = "({query})".format(query=querystring, **kwargs)

        if with_alias:
            return format_alias_sql(querystring, self.alias or self._table_name, **kwargs)

        return querystring