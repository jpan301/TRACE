def where_in_quote(self, *args, **kwargs):
    def quote(value: Any) -> str:
        if isinstance(value, str):
            value = value.replace(mark, mark * 2)
            return f"{mark}{value}{mark}"
        return str(value)
