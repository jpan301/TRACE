# source: DjangoSafe / django/shortcuts.py
# function: aget_list_or_404

async def aget_list_or_404(klass, *args, **kwargs):
    """See get_list_or_404()."""
    queryset = _get_queryset(klass)
    if not hasattr(queryset, "filter"):
        klass__name = (
            klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        )
        raise ValueError(
            "First argument to aget_list_or_404() must be a Model, Manager, or "
            f"QuerySet, not '{klass__name}'."
        )
    obj_list = [obj async for obj in queryset.filter(*args, **kwargs)]
    if not obj_list:
        raise Http404(
            _("No %s matches the given query.") % queryset.model._meta.object_name
        )
    return obj_list