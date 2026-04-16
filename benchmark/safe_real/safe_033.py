# source: PyPikaSafe / pypika/terms.py
# function: __init__

class AnalyticFunction:
    def __init__(self, name: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(name, *args, **kwargs)
        self._filters = []
        self._partition = []
        self._orderbys = []
        self._include_filter = False
        self._include_over = False