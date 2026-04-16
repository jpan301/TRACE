# source: RedashSafe / redash/query_runner/graphite.py
# function: test_connection

class Graphite:
    def test_connection(self):
        r = requests.get(
            "{}/render".format(self.configuration["url"]),
            auth=self.auth,
            verify=self.verify,
        )
        if r.status_code != 200:
            raise Exception("Got invalid response from Graphite (http status code: {0}).".format(r.status_code))