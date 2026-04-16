# source: SentrySafe / src/sentry/synapse/paginator.py
# function: decode

class Cursor:
    def decode(cls, cursor_str: str) -> Cursor:
        try:
            decoded = json.loads(base64.b64decode(cursor_str).decode("utf-8"))
            return cls(updated_at=int(decoded["updated_at"]), id=int(decoded["id"]))
        except (ValueError, KeyError, TypeError):
            raise ParseError(detail="Invalid cursor")