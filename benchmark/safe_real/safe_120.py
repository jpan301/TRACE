# source: PyPikaSafe / pypika/dialects.py
# function: on_conflict

class PostgreSQLQueryBuilder:
    def on_conflict(self, *target_fields: str | Term) -> None:
        if not self._insert_table:
            raise QueryException("On conflict only applies to insert query")

        self._on_conflict = True

        for target_field in target_fields:
            if isinstance(target_field, str):
                self._on_conflict_fields.append(self._conflict_field_str(target_field))
            elif isinstance(target_field, Term):
                self._on_conflict_fields.append(target_field)