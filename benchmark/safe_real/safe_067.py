# source: DjangoSafe / django/db/backends/base/schema.py
# function: _index_include_sql

class BaseDatabaseSchemaEditor:
    def _index_include_sql(self, model, columns):
        if not columns or not self.connection.features.supports_covering_indexes:
            return ""
        return Statement(
            " INCLUDE (%(columns)s)",
            columns=Columns(model._meta.db_table, columns, self.quote_name),
        )