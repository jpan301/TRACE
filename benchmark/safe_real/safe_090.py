# source: PyPikaSafe / pypika/queries.py
# function: from_

class QueryBuilder:
    def from_(self, selectable: Selectable | Query | str) -> None:
        """
        Adds a table to the query. This function can only be called once and will raise an AttributeError if called a
        second time.

        :param selectable:
            Type: ``Table``, ``Query``, or ``str``

            When a ``str`` is passed, a table with the name matching the ``str`` value is used.

        :returns
            A copy of the query with the table added.
        """

        self._from.append(Table(selectable) if isinstance(selectable, str) else selectable)

        if isinstance(selectable, (QueryBuilder, _SetOperation)) and selectable.alias is None:
            if isinstance(selectable, QueryBuilder):
                sub_query_count = selectable._subquery_count
            else:
                sub_query_count = 0

            sub_query_count = max(self._subquery_count, sub_query_count)
            selectable.alias = "sq%d" % sub_query_count
            self._subquery_count = sub_query_count + 1