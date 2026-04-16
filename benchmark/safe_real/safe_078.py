# source: RedashSafe / redash/query_runner/corporate_memory.py
# function: _setup_environment

class CorporateMemoryQueryRunner:
    def _setup_environment(self):
        """provide environment for cmempy

        cmempy environment variables need to match key in the properties
        object of the configuration_schema
        """
        for key in self.KNOWN_CONFIG_KEYS:
            if key in environ:
                environ.pop(key)
            value = self.configuration.get(key, None)
            if value is not None:
                environ[key] = str(value)
                if key in self.KNOWN_SECRET_KEYS:
                    logger.info("{} set by config".format(key))
                else:
                    logger.info("{} set by config to {}".format(key, environ[key]))