# source: PyPikaSafe / pypika/queries.py
# function: __init__

class Table:
    def __init__(
        self,
        name: str,
        schema: Schema | str | None = None,
        alias: str | None = None,
        query_cls: type[Query] | None = None,
    ) -> None:
        super().__init__(alias)
        self._table_name = name
        self._schema = self._init_schema(schema)
        self._query_cls = query_cls or Query
        self._for = None
        self._for_portion = None
        if not issubclass(self._query_cls, Query):
            raise TypeError("Expected 'query_cls' to be subclass of Query")