def _convert_field_to_tz(self, *args, **kwargs):
    def _convert_field_to_tz(self, sql, params, tzname):
        if tzname and settings.USE_TZ and self.connection.timezone_name != tzname:
            return f"CONVERT_TZ({sql}, %s, %s)", (
                *params,
                self.connection.timezone_name,
                self._prepare_tzname_delta(tzname),
            )
        return sql, params
