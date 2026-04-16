# source: RedashSafe / redash/query_runner/google_analytics4.py
# function: get_formatted_column_json

def get_formatted_column_json(column_name):
    data_type = None

    if column_name == "date":
        data_type = "DATE"
    elif column_name == "dateHour":
        data_type = "DATETIME"

    result = {
        "name": column_name,
        "friendly_name": column_name,
        "type": types_conv.get(data_type, "string"),
    }

    return result