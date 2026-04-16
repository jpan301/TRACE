# source: SentrySafe / src/sentry/utils/marketo_client.py
# function: make_request

class MarketoClient:
    def make_request(self, url: str, *args, method="GET", **kwargs):
        base_url = settings.MARKETO_BASE_URL or ""
        full_url = base_url + url
        session = http.build_session()
        resp = getattr(session, method.lower())(full_url, *args, **kwargs)
        resp.raise_for_status()
        return resp.json()