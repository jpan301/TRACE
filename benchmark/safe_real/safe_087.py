# source: PyPikaSafe / pypika/dialects.py
# function: get_value_sql

class SQLLiteValueWrapper:
    def get_value_sql(self, **kwargs: Any) -> str:
        if isinstance(self.value, bool):
            return "1" if self.value else "0"
        return super().get_value_sql(**kwargs)