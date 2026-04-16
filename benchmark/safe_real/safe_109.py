# source: DjangoSafe / django/core/serializers/__init__.py
# function: get_public_serializer_formats

def get_public_serializer_formats():
    if not _serializers:
        _load_serializers()
    return [k for k, v in _serializers.items() if not v.Serializer.internal_use_only]