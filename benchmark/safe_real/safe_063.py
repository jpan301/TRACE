# source: RedashSafe / redash/query_runner/databricks.py
# function: run_query

class Databricks:
    def run_query(self, query, user):
        try:
            cursor = self._get_cursor()

            statements = split_sql_statements(query)
            for stmt in statements:
                cursor.execute(stmt)

            if cursor.description is not None:
                result_set = cursor.fetchmany(ROW_LIMIT)
                columns = self.fetch_columns([(i[0], TYPES_MAP.get(i[1], TYPE_STRING)) for i in cursor.description])

                rows = [dict(zip((column["name"] for column in columns), row)) for row in result_set]

                data = {"columns": columns, "rows": rows}

                if len(result_set) >= ROW_LIMIT and cursor.fetchone() is not None:
                    logger.warning("Truncated result set.")
                    statsd_client.incr("redash.query_runner.databricks.truncated")
                    data["truncated"] = True
                error = None
            else:
                error = None
                data = {
                    "columns": [{"name": "result", "type": TYPE_STRING}],
                    "rows": [{"result": "No data was returned."}],
                }

            cursor.close()
        except pyodbc.Error as e:
            if len(e.args) > 1:
                error = str(e.args[1])
            else:
                error = str(e)
            data = None

        return data, error