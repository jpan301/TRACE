# source: RedashSafe / redash/models/changes.py
# function: prep_cleanvalues

class ChangeTrackingMixin:
    def prep_cleanvalues(self):
        self.__dict__["_clean_values"] = {}
        for attr in inspect(self.__class__).column_attrs:
            (col,) = attr.columns
            # 'query' is col name but not attr name
            self._clean_values[col.name] = None