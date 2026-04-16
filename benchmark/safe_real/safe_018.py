# source: RedashSafe / redash/query_runner/pinot.py
# function: get_schema

class Pinot:
    def get_schema(self, get_stats=False):
        schema = {}
        for schema_name in self.get_schema_names():
            for table_name in self.get_table_names():
                schema_table_name = "{}.{}".format(schema_name, table_name)
                if table_name not in schema:
                    schema[schema_table_name] = {"name": schema_table_name, "columns": []}
                table_schema = self.get_pinot_table_schema(table_name)

                for column in (
                    table_schema.get("dimensionFieldSpecs", [])
                    + table_schema.get("metricFieldSpecs", [])
                    + table_schema.get("dateTimeFieldSpecs", [])
                ):
                    c = {
                        "name": column["name"],
                        "type": PINOT_TYPES_MAPPING[column["dataType"]],
                    }
                    schema[schema_table_name]["columns"].append(c)
        return list(schema.values())