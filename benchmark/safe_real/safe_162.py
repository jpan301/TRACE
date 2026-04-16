# source: RedashSafe / redash/query_runner/google_analytics.py
# function: test_connection

class GoogleAnalytics:
    def test_connection(self):
        try:
            service = self._get_analytics_service()
            service.management().accounts().list().execute()
        except HttpError as e:
            # Make sure we return a more readable error to the end user
            raise Exception(e._get_reason())