# source: SentrySafe / src/sentry/snuba/metrics_layer/query.py
# function: run_query

def run_query(request: Request) -> Mapping[str, Any]:
    """
    Entrypoint for executing a metrics query in Snuba.
    """
    return bulk_run_query([request])[0]