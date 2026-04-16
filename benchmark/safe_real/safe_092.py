# source: DjangoSafe / django/db/models/fields/__init__.py
# function: get_db_prep_value

class TimeField:
    def get_db_prep_value(self, value, connection, prepared=False):
        # Casts times into the format expected by the backend
        if not prepared:
            value = self.get_prep_value(value)
        return connection.ops.adapt_timefield_value(value)