# source: PyPikaSafe / pypika/queries.py
# function: validate

class JoinOn:
    def validate(self, _from: Sequence[Table], _joins: Sequence[Table]) -> None:
        criterion_tables = set([f.table for f in self.criterion.fields_()])
        available_tables = set(_from) | {join.item for join in _joins} | {self.item}
        missing_tables = criterion_tables - available_tables
        if missing_tables:
            raise JoinException(
                "Invalid join criterion. One field is required from the joined item and "
                "another from the selected table or an existing join.  Found [{tables}]".format(
                    tables=", ".join(map(str, missing_tables))
                )
            )