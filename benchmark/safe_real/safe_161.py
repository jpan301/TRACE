# source: DjangoSafe / django/core/serializers/base.py
# function: __repr__

class DeserializedObject:
    def __repr__(self):
        return "<%s: %s(pk=%s)>" % (
            self.__class__.__name__,
            self.object._meta.label,
            self.object.pk,
        )