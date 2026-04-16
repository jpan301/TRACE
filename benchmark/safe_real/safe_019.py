# source: PyPikaSafe / pypika/queries.py
# function: into

class Query:
    def into(cls, table: Table | str, **kwargs: Any) -> QueryBuilder:
        """
        Query builder entry point.  Initializes query building and sets the table to insert into.  When using this
        function, the query becomes an INSERT query.

        :param table:
            Type: Table or str

            An instance of a Table object or a string table name.

        :return QueryBuilder
        """
        return cls._builder(**kwargs).into(table)