# source: RedashSafe / redash/query_runner/influx_db_v2.py
# function: _get_data_from_tables

class InfluxDBv2:
    def _get_data_from_tables(self, tables: Any) -> Dict:
        """
        Determines the data of the given tables in an appropriate schema for
        redash ui to render it. It retrieves all available columns and records
        from the tables.
        :param tables: A list of FluxTable instances.
        :return: An object with columns and rows list.
        """
        columns = []
        rows = []

        for table in tables:
            for column in table.columns:
                column_entry = {
                    "name": column.label,
                    "type": self._get_type(column.data_type),
                    "friendly_name": column.label.title(),
                }
                if column_entry not in columns:
                    columns.append(column_entry)

            rows.extend([row.values for row in [record for record in table.records]])

        return {"columns": columns, "rows": rows}