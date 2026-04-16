# source: DjangoSafe / django/core/serializers/__init__.py
# function: get_deserializer

def get_deserializer(format):
    if not _serializers:
        _load_serializers()
    if format not in _serializers:
        raise SerializerDoesNotExist(format)
    return _serializers[format].Deserializer