# source: PyPikaSafe / pypika/queries.py
# function: update

class Query:
    def update(cls, table: str | Table, **kwargs) -> QueryBuilder:
        """
        Query builder entry point.  Initializes query building and sets the table to update.  When using this
        function, the query becomes an UPDATE query.

        :param table:
            Type: Table or str

            An instance of a Table object or a string table name.

        :return: QueryBuilder
        """
        return cls._builder(**kwargs).update(table)