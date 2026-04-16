def where_in(values: List[Any], mark: str = "'") -> str:
    """
    Given a list of values, build a parenthesis list suitable for an IN expression.

        >>> where_in([1, "b", 3])
        (1, 'b', 3)

    """

    def quote(value: Any) -> str:
        if isinstance(value, str):
            value = value.replace(mark, mark * 2)
            return f"{mark}{value}{mark}"
        return str(value)

    joined_values = ", ".join(quote(value) for value in values)
    return f"({joined_values})"
