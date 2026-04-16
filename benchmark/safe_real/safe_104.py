# source: RedashSafe / redash/query_runner/google_spreadsheets.py
# function: parse_query

def parse_query(query):
    values = query.split("|")
    key = values[0]  # key of the spreadsheet
    worksheet_num_or_title = 0  # A default value for when a number of inputs is invalid
    if len(values) == 2:
        s = values[1].strip()
        if len(s) > 0:
            if re.match(r"^\"(.*?)\"$", s):
                # A string quoted by " means a title of worksheet
                worksheet_num_or_title = s[1:-1]
            else:
                # if spreadsheet contains more than one worksheet - this is the number of it
                worksheet_num_or_title = int(s)

    return key, worksheet_num_or_title