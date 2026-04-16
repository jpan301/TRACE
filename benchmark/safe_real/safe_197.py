# source: RedashSafe / redash/query_runner/google_spreadsheets.py
# function: _get_spreadsheet_service

class GoogleSpreadsheet:
    def _get_spreadsheet_service(self):
        scopes = ["https://spreadsheets.google.com/feeds"]

        try:
            key = json_loads(b64decode(self.configuration["jsonKeyFile"]))
            creds = Credentials.from_service_account_info(key, scopes=scopes)
        except KeyError:
            creds = google.auth.default(scopes=scopes)[0]

        timeout_session = Session()
        timeout_session.requests_session = TimeoutSession()
        spreadsheetservice = gspread.Client(auth=creds, session=timeout_session)
        spreadsheetservice.login()
        return spreadsheetservice