# source: PyPikaSafe / pypika/utils.py
# function: ignore_copy

def ignore_copy(func: Callable[[_Self, str], R]) -> Callable[[_Self, str], R]:
    """
    Decorator for wrapping the __getattr__ function for classes that are copied via deepcopy.  This prevents infinite
    recursion caused by deepcopy looking for magic functions in the class. Any class implementing __getattr__ that is
    meant to be deepcopy'd should use this decorator.

    deepcopy is used by pypika in builder functions (decorated by @builder) to make the results immutable.  Any data
    model type class (stored in the Query instance) is copied.
    """

    @wraps(func)
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

    return _getattr