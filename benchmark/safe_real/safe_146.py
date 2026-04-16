# source: PyPikaSafe / pypika/terms.py
# function: replace_table

class Term:
    def replace_table(self, current_table: Table | None, new_table: Table | None) -> Term:
        """
        Replaces all occurrences of the specified table with the new table. Useful when reusing fields across queries.
        The base implementation returns self because not all terms have a table property.

        :param current_table:
            The table to be replaced.
        :param new_table:
            The table to replace with.
        :return:
            Self.
        """
        return self