# source: PyPikaSafe / pypika/terms.py
# function: replace_table

class Field:
    def replace_table(self, current_table: Table | None, new_table: Table | None) -> None:
        """
        Replaces all occurrences of the specified table with the new table. Useful when reusing fields across queries.

        :param current_table:
            The table to be replaced.
        :param new_table:
            The table to replace with.
        :return:
            A copy of the field with the tables replaced.
        """
        self.table = new_table if self.table == current_table else self.table