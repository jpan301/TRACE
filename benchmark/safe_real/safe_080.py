# source: RedashSafe / redash/query_runner/influx_db.py
# function: _transform_result

def _transform_result(results):
    column_names = []
    result_rows = []

    for result in results:
        for series in result.raw.get("series", []):
            for column in series["columns"]:
                if column not in column_names:
                    column_names.append(column)
            tags = series.get("tags", {})
            for key in tags.keys():
                if key not in column_names:
                    column_names.append(key)

    for result in results:
        for series in result.raw.get("series", []):
            for point in series["values"]:
                result_row = {}
                for column in column_names:
                    tags = series.get("tags", {})
                    if column in tags:
                        result_row[column] = tags[column]
                    elif column in series["columns"]:
                        index = series["columns"].index(column)
                        value = point[index]
                        result_row[column] = value
                result_rows.append(result_row)

    if len(result_rows) > 0:
        result_columns = [{"name": c, "type": _get_type(result_rows[0][c])} for c in result_rows[0].keys()]
    else:
        result_columns = [{"name": c, "type": TYPE_STRING} for c in column_names]

    return {"columns": result_columns, "rows": result_rows}