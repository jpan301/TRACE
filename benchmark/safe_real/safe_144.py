# source: DjangoSafe / django/db/models/query.py
# function: _avoid_cloning

class QuerySet:
    def _avoid_cloning(self):
        """
        Temporarily prevent QuerySet _clone() operations, restoring the default
        behavior on exit. For the duration of the context managed statement,
        all operations (e.g. filter(), exclude(), etc.) will mutate the same
        QuerySet instance.

        @contextlib.contextmanager is intentionally not used for performance
        reasons.
        """
        return PreventQuerySetCloning(self)