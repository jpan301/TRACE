# source: DjangoSafe / django/db/models/fields/related_lookups.py
# function: as_sql

class RelatedLookupMixin:
    def as_sql(self, compiler, connection):
        if isinstance(self.lhs, ColPairs):
            if not self.rhs_is_direct_value():
                raise ValueError(
                    f"'{self.lookup_name}' doesn't support multi-column subqueries."
                )
            self.rhs = get_normalized_value(self.rhs, self.lhs)
            lookup_class = tuple_lookups[self.lookup_name]
            lookup = lookup_class(self.lhs, self.rhs)
            return compiler.compile(lookup)

        return super().as_sql(compiler, connection)