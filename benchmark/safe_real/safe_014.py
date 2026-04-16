# source: DjangoSafe / django/utils/inspect.py
# function: signature

def signature(obj):
    """
    A wrapper around inspect.signature that leaves deferred annotations
    unevaluated on Python 3.14+, since they are not used in our case.
    """
    if PY314:
        return inspect.signature(obj, annotation_format=annotationlib.Format.FORWARDREF)
    else:
        return inspect.signature(obj)