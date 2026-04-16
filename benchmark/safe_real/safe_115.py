# source: SentrySafe / src/sentry/snuba/entity_subscription.py
# function: get_entity_subscription

def get_entity_subscription(
    query_type: SnubaQuery.Type,
    dataset: Dataset,
    aggregate: str,
    time_window: int,
    extra_fields: _EntitySpecificParams | None = None,
) -> EntitySubscription:
    """
    Function that routes to the correct instance of `EntitySubscription` based on the query type and
    dataset, and additionally does validation on aggregate for the sessions and metrics datasets
    then returns the instance of `EntitySubscription`
    """
    entity_subscription_cls: type[EntitySubscription] | None = None
    if query_type == SnubaQuery.Type.ERROR:
        entity_subscription_cls = EventsEntitySubscription
    if query_type == SnubaQuery.Type.PERFORMANCE:
        if dataset == Dataset.Transactions:
            entity_subscription_cls = PerformanceTransactionsEntitySubscription
        elif dataset in (Dataset.Metrics, Dataset.PerformanceMetrics):
            entity_subscription_cls = PerformanceMetricsEntitySubscription
        elif dataset == Dataset.EventsAnalyticsPlatform:
            entity_subscription_cls = PerformanceSpansEAPRpcEntitySubscription
    if query_type == SnubaQuery.Type.CRASH_RATE:
        entity_key = determine_crash_rate_alert_entity(aggregate)
        if entity_key == EntityKey.MetricsCounters:
            entity_subscription_cls = MetricsCountersEntitySubscription
        if entity_key == EntityKey.MetricsSets:
            entity_subscription_cls = MetricsSetsEntitySubscription

    if entity_subscription_cls is None:
        raise UnsupportedQuerySubscription(
            f"Couldn't determine entity subscription for query type {query_type} with dataset {dataset}"
        )

    return entity_subscription_cls(aggregate, time_window, extra_fields)