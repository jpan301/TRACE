# source: SentrySafe / src/sentry/search/events/builder/base.py
# function: resolve_boolean_condition

class BaseQueryBuilder:
    def resolve_boolean_condition(
        self, term: event_filter.ParsedTerm
    ) -> tuple[list[WhereType], list[WhereType]]:
        if isinstance(term, event_search.ParenExpression):
            return self.resolve_boolean_conditions(term.children)

        where, having = [], []

        if isinstance(term, event_search.SearchFilter):
            where = self.resolve_where([term])
        elif isinstance(term, event_search.AggregateFilter):
            having = self.resolve_having([term])

        return where, having