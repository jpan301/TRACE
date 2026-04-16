# source: SentrySafe / src/sentry/snuba/metrics/fields/snql.py
# function: crashed_users

def crashed_users(org_id: int, metric_ids: Sequence[int], alias: str | None = None) -> Function:
    return _set_uniq_aggregation_on_session_status_factory(
        org_id, session_status="crashed", metric_ids=metric_ids, alias=alias
    )