# source: DjangoSafe / django/db/models/sql/query.py
# function: get_columns

class RawQuery:
    def get_columns(self):
        if self.cursor is None:
            self._execute_query()
        converter = connections[self.using].introspection.identifier_converter
        return [converter(column_meta[0]) for column_meta in self.cursor.description]