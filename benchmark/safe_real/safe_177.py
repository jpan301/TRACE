# source: DjangoSafe / django/db/backends/sqlite3/schema.py
# function: delete_model

class DatabaseSchemaEditor:
    def delete_model(self, model, handle_autom2m=True):
        if handle_autom2m:
            super().delete_model(model)
        else:
            # Delete the table (and only that)
            self.execute(
                self.sql_delete_table
                % {
                    "table": self.quote_name(model._meta.db_table),
                }
            )
            # Remove all deferred statements referencing the deleted table.
            for sql in list(self.deferred_sql):
                if isinstance(sql, Statement) and sql.references_table(
                    model._meta.db_table
                ):
                    self.deferred_sql.remove(sql)