# source: DjangoSafe / django/contrib/gis/db/backends/spatialite/base.py
# function: get_new_connection

class DatabaseWrapper:
    def get_new_connection(self, conn_params):
        conn = super().get_new_connection(conn_params)
        # Enabling extension loading on the SQLite connection.
        try:
            conn.enable_load_extension(True)
        except AttributeError:
            raise ImproperlyConfigured(
                "SpatiaLite requires SQLite to be configured to allow "
                "extension loading."
            )
        # Load the SpatiaLite library extension on the connection.
        for path in self.lib_spatialite_paths:
            try:
                conn.load_extension(path)
            except Exception:
                if getattr(settings, "SPATIALITE_LIBRARY_PATH", None):
                    raise ImproperlyConfigured(
                        "Unable to load the SpatiaLite library extension "
                        "as specified in your SPATIALITE_LIBRARY_PATH setting."
                    )
                continue
            else:
                break
        else:
            raise ImproperlyConfigured(
                "Unable to load the SpatiaLite library extension. "
                "Library names tried: %s" % ", ".join(self.lib_spatialite_paths)
            )
        return conn