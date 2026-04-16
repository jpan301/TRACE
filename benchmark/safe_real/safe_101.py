# source: PyPikaSafe / pypika/queries.py
# function: _table_options_sql

class CreateQueryBuilder:
    def _table_options_sql(self, **kwargs) -> str:
        table_options = ""

        if self._with_system_versioning:
            table_options += ' WITH SYSTEM VERSIONING'

        return table_options