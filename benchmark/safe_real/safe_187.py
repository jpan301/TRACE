# source: DjangoSafe / django/db/models/expressions.py
# function: copy

class Subquery:
    def copy(self):
        clone = super().copy()
        clone.query = clone.query.clone()
        return clone