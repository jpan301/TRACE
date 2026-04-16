# source: PyPikaSafe / pypika/queries.py
# function: pipe

class QueryBuilder:
    def pipe(self, func, *args, **kwargs):
        """Call a function on the current object and return the result.

        Example usage:

        .. code-block:: python

            from pypika import Query, functions as fn
            from pypika.queries import QueryBuilder

            def rows_by_group(query: QueryBuilder, *groups) -> QueryBuilder:
                return (
                    query
                    .select(*groups, fn.Count("*").as_("n_rows"))
                    .groupby(*groups)
                )

            base_query = Query.from_("table")

            col1_agg = base_query.pipe(rows_by_group, "col1")
            col2_agg = base_query.pipe(rows_by_group, "col2")
            col1_col2_agg = base_query.pipe(rows_by_group, "col1", "col2")

        Makes chaining functions together easier, especially when the functions are
        defined elsewhere. For example, you could define a function that filters
        rows by a date range and then group by a set of columns:


        .. code-block:: python

            from datetime import datetime, timedelta

            from pypika import Field

            def days_since(query: QueryBuilder, n_days: int) -> QueryBuilder:
                return (
                    query
                    .where("date" > fn.Date(datetime.now().date() - timedelta(days=n_days)))
                )

            (
                base_query
                .pipe(days_since, n_days=7)
                .pipe(rows_by_group, "col1", "col2")
            )
        """
        return func(self, *args, **kwargs)