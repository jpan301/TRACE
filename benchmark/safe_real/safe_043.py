# source: PyPikaSafe / pypika/terms.py
# function: replace_table

class ContainsCriterion:
    def replace_table(self, current_table: Table | None, new_table: Table | None) -> None:
        """
        Replaces all occurrences of the specified table with the new table. Useful when reusing fields across queries.

        :param current_table:
            The table to be replaced.
        :param new_table:
            The table to replace with.
        :return:
            A copy of the criterion with the tables replaced.
        """
        self.term = self.term.replace_table(current_table, new_table)