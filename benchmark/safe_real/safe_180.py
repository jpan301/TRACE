# source: RedashSafe / redash/query_runner/ignite.py
# function: configuration_schema

class Ignite:
    def configuration_schema(cls):
        return {
            "type": "object",
            "properties": {
                "user": {"type": "string"},
                "password": {"type": "string"},
                "server": {"type": "string", "default": "127.0.0.1:10800"},
                "tls": {"type": "boolean", "default": False, "title": "Use SSL/TLS connection"},
                "schema": {"type": "string", "title": "Schema Name", "default": "PUBLIC"},
                "distributed_joins": {"type": "boolean", "title": "Allow distributed joins", "default": False},
                "enforce_join_order": {"type": "boolean", "title": "Enforce join order", "default": False},
                "lazy": {"type": "boolean", "title": "Lazy query execution", "default": True},
                "gridgain": {"type": "boolean", "title": "Use GridGain libraries", "default": gridgain_available},
            },
            "required": ["server"],
            "secret": ["password"],
        }