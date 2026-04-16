# source: DjangoSafe / django/db/models/lookups.py
# function: select_format

class Lookup:
    def select_format(self, compiler, sql, params):
        # Wrap filters with a CASE WHEN expression if a database backend
        # (e.g. Oracle) doesn't support boolean expression in SELECT or GROUP
        # BY list.
        if not compiler.connection.features.supports_boolean_expr_in_select_clause:
            sql = f"CASE WHEN {sql} THEN 1 ELSE 0 END"
        return sql, params