# source: PyPikaSafe / pypika/queries.py
# function: select

class Query:
    def select(cls, *terms: int | float | str | bool | Term, **kwargs: Any) -> QueryBuilder:
        """
        Query builder entry point.  Initializes query building without a table and selects fields.  Useful when testing
        SQL functions.

        :param terms:
            Type: list[expression]

            A list of terms to select.  These can be any type of int, float, str, bool, or Term.  They cannot be a Field
            unless the function ``Query.from_`` is called first.

        :return: QueryBuilder
        """
        return cls._builder(**kwargs).select(*terms)