# source: RedashSafe / redash/query_runner/tinybird.py
# function: _get_from_tinybird

class Tinybird:
    def _get_from_tinybird(self, endpoint, params=None):
        url = f"{self.configuration.get('url', self.DEFAULT_URL)}{endpoint}"
        authorization = f"Bearer {self.configuration.get('token')}"

        try:
            response = requests.get(
                url,
                timeout=self.configuration.get("timeout", 30),
                params=params,
                headers={"Authorization": authorization},
                verify=self.configuration.get("verify", True),
            )
        except requests.RequestException as e:
            if e.response:
                details = f"({e.__class__.__name__}, Status Code: {e.response.status_code})"
            else:
                details = f"({e.__class__.__name__})"
            raise Exception(f"Connection error to: {url} {details}.")

        if response.status_code >= 400:
            raise Exception(response.text)

        return response.json()