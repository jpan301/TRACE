# source: PyPikaSafe / pypika/terms.py
# function: __init__

class Function:
    def __init__(self, name: str, *args: Any, **kwargs: Any) -> None:
        super().__init__(kwargs.get("alias"))
        self.name = name
        self.args = [self.wrap_constant(param) for param in args]
        self.schema = kwargs.get("schema")