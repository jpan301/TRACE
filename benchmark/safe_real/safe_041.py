# source: PyPikaSafe / pypika/queries.py
# function: foreign_key

class CreateQueryBuilder:
    def foreign_key(
        self,
        columns: list[str | Column],
        reference_table: str | Table,
        reference_columns: list[str | Column],
        on_delete: ReferenceOption = None,
        on_update: ReferenceOption = None,
    ) -> None:
        """
        Adds a foreign key constraint.

        :param columns:
            Type:  List[Union[str, Column]]

            A list of foreign key columns.

        :param reference_table:
            Type: Union[str, Table]

            The parent table name.

        :param reference_columns:
            Type: List[Union[str, Column]]

            Parent key columns.

        :param on_delete:
            Type: ReferenceOption

            Delete action.

        :param on_update:
            Type: ReferenceOption

            Update option.

        :raises AttributeError:
            If the foreign key is already defined.

        :return:
            CreateQueryBuilder.
        """
        if self._foreign_key:
            raise AttributeError("'Query' object already has attribute foreign_key")
        self._foreign_key = self._prepare_columns_input(columns)
        self._foreign_key_reference_table = reference_table
        self._foreign_key_reference = self._prepare_columns_input(reference_columns)
        self._foreign_key_on_delete = on_delete
        self._foreign_key_on_update = on_update