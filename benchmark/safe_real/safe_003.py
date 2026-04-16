# source: RedashSafe / redash/query_runner/athena.py
# function: get_schema

class Athena:
    def get_schema(self, get_stats=False):
        if self.configuration.get("glue", False):
            catalog_ids = [id.strip() for id in self.configuration.get("catalog_ids", "").split(",")]
            return sum([self.__get_schema_from_glue(catalog_id) for catalog_id in catalog_ids], [])

        schema = {}
        query = """
        SELECT table_schema, table_name, column_name, data_type
        FROM information_schema.columns
        WHERE table_schema NOT IN ('information_schema')
        """

        results, error = self.run_query(query, None)
        if error is not None:
            self._handle_run_query_error(error)

        for row in results["rows"]:
            table_name = "{0}.{1}".format(row["table_schema"], row["table_name"])
            if table_name not in schema:
                schema[table_name] = {"name": table_name, "columns": []}
            schema[table_name]["columns"].append({"name": row["column_name"], "type": row["data_type"]})

        return list(schema.values())