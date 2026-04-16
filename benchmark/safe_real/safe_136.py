# source: PyPikaSafe / pypika/utils.py
# function: _getattr

class DummyClass:
    def _getattr(self, name: str) -> R:
        if name in [
            "__copy__",
            "__deepcopy__",
            "__getstate__",
            "__setstate__",
            "__getnewargs__",
        ]:
            raise AttributeError("'%s' object has no attribute '%s'" % (self.__class__.__name__, name))

        return func(self, name)