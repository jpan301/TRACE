# source: SentrySafe / src/sentry/sentry_apps/tasks/service_hooks.py
# function: _get_service_hooks

def _get_service_hooks(project_id: int) -> list[tuple[int, list[str]]]:
    from sentry.sentry_apps.models.servicehook import ServiceHook

    cache_key = f"servicehooks:1:{project_id}"
    result = cache.get(cache_key)

    if result is None:
        hooks = ServiceHook.objects.filter(servicehookproject__project_id=project_id)
        result = [(h.id, h.events) for h in hooks]
        cache.set(cache_key, result, 60)
    return result