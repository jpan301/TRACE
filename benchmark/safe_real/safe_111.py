# source: SentrySafe / src/sentry/snuba/metrics/naming_layer/mapping.py
# function: create_name_mapping_layers

def create_name_mapping_layers() -> None:
    # ToDo(ahmed): Hack this out once the FE changes their mappings
    # Backwards Compat
    NAME_TO_MRI.update(
        {
            # Session
            "sentry.sessions.session": SessionMRI.RAW_SESSION,
            "sentry.sessions.user": SessionMRI.RAW_USER,
            "sentry.sessions.session.duration": SessionMRI.RAW_DURATION,
            "sentry.sessions.session.error": SessionMRI.RAW_ERROR,
        }
    )

    for MetricKey, MRI in (
        (SessionMetricKey, SessionMRI),
        (TransactionMetricKey, TransactionMRI),
        (SpanMetricKey, SpanMRI),
    ):
        # Adds new names at the end, so that when the reverse mapping is created
        for metric_key in MetricKey:
            NAME_TO_MRI[metric_key.value] = MRI[metric_key.name]

    MRI_TO_NAME.update({v.value: k for k, v in NAME_TO_MRI.items()})