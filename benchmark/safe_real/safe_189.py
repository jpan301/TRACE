# source: RedashSafe / redash/query_runner/duckdb.py
# function: run_query

class DuckDB:
    def run_query(self, query, user) -> tuple:
        try:
            cursor = self.con.cursor()
            cursor.execute(query)
            columns = self.fetch_columns(
                [(d[0], TYPES_MAP.get(d[1].upper(), TYPE_STRING)) for d in cursor.description]
            )
            rows = [dict(zip((col["name"] for col in columns), row)) for row in cursor.fetchall()]
            data = {"columns": columns, "rows": rows}
            return data, None
        except duckdb.InterruptException:
            raise InterruptException("Query cancelled by user.")
        except Exception as e:
            logger.exception("Error running query: %s", e)
            return None, str(e)