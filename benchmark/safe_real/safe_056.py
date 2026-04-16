# source: RedashSafe / redash/query_runner/__init__.py
# function: host

class BaseQueryRunner:
    def host(self):
        """Returns this query runner's configured host.
        This is used primarily for temporarily swapping endpoints when using SSH tunnels to connect to a data source.

        `BaseQueryRunner`'s naïve implementation supports query runner implementations that store endpoints using `host` and `port`
        configuration values. If your query runner uses a different schema (e.g. a web address), you should override this function.
        """
        if "host" in self.configuration:
            return self.configuration["host"]
        else:
            raise NotImplementedError()