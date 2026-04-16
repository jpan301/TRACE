# source: RedashSafe / redash/query_runner/databend.py
# function: _get_tables

class Databend:
    def _get_tables(self):
        query = """
        SELECT TABLE_SCHEMA,
               TABLE_NAME,
               COLUMN_NAME
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA NOT IN ('information_schema', 'system')
        """

        results, error = self.run_query(query, None)

        if error is not None:
            self._handle_run_query_error(error)

        schema = {}

        for row in results["rows"]:
            table_name = "{}.{}".format(row["table_schema"], row["table_name"])

            if table_name not in schema:
                schema[table_name] = {"name": table_name, "columns": []}

            schema[table_name]["columns"].append(row["column_name"])

        return list(schema.values())