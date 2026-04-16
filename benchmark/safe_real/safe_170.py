# source: PyPikaSafe / pypika/queries.py
# function: as_select

class CreateQueryBuilder:
    def as_select(self, query_builder: QueryBuilder) -> None:
        """
        Creates the table from a select statement.

        :param query_builder:
            The query.

        :raises AttributeError:
            If columns have been defined for the table.

        :return:
            CreateQueryBuilder.
        """
        if self._columns:
            raise AttributeError("'Query' object already has attribute columns")

        if not isinstance(query_builder, QueryBuilder):
            raise TypeError("Expected 'item' to be instance of QueryBuilder")

        self._as_select = query_builder