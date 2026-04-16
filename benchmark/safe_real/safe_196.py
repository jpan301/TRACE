# source: DjangoSafe / django/db/backends/base/introspection.py
# function: get_primary_key_column

class BaseDatabaseIntrospection:
    def get_primary_key_column(self, cursor, table_name):
        """
        Return the name of the primary key column for the given table.
        """
        columns = self.get_primary_key_columns(cursor, table_name)
        return columns[0] if columns else None