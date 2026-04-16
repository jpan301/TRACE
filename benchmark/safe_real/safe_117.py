# source: DjangoSafe / django/db/models/sql/subqueries.py
# function: _setup_query

class UpdateQuery:
    def _setup_query(self):
        """
        Run on initialization and at the end of chaining. Any attributes that
        would normally be set in __init__() should go here instead.
        """
        self.values = []
        self.related_ids = None
        self.related_updates = {}