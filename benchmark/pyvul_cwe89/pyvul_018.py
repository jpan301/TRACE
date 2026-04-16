def __init__(self, *args, **kwargs):
    def __init__(
        self,
        database: "Database",
        query: Optional["Query"] = None,
        table: Optional["SqlaTable"] = None,
        extra_cache_keys: Optional[list[Any]] = None,
        removed_filters: Optional[list[str]] = None,
        applied_filters: Optional[list[str]] = None,
        **kwargs: Any,
    ) -> None:
        self._database = database
        self._query = query
        self._schema = None
        if query and query.schema:
            self._schema = query.schema
        elif table:
            self._schema = table.schema
        self._extra_cache_keys = extra_cache_keys
        self._applied_filters = applied_filters
        self._removed_filters = removed_filters
        self._context: dict[str, Any] = {}
        self._env = SandboxedEnvironment(undefined=DebugUndefined)
        self.set_context(**kwargs)

        # custom filters
        self._env.filters["where_in"] = where_in
