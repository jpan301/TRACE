# source: PyPikaSafe / pypika/queries.py
# function: __repr__

class Table:
    def __repr__(self) -> str:
        if self._schema:
            return "Table('{}', schema='{}')".format(self._table_name, self._schema)
        return "Table('{}')".format(self._table_name)