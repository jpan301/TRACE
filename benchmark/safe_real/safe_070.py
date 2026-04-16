# source: PyPikaSafe / pypika/dialects.py
# function: _validate_returning_term

class PostgreSQLQueryBuilder:
    def _validate_returning_term(self, term: Term) -> None:
        for field in term.fields_():
            if not any([self._insert_table, self._update_table, self._delete_from]):
                raise QueryException("Returning can't be used in this query")

            table_is_insert_or_update_table = field.table in {self._insert_table, self._update_table}
            join_tables = set(itertools.chain.from_iterable([j.criterion.tables_ for j in self._joins]))
            join_and_base_tables = set(self._from) | join_tables
            table_not_base_or_join = bool(term.tables_ - join_and_base_tables)
            if not table_is_insert_or_update_table and table_not_base_or_join:
                raise QueryException("You can't return from other tables")