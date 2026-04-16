# source: SentrySafe / src/sentry/sentry_apps/api/utils/webhook_requests.py
# function: get_buffer_requests_from_control

def get_buffer_requests_from_control(
    sentry_app: SentryApp,
    filter: SentryAppRequestFilterArgs,
    datetime_org_filter: DatetimeOrganizationFilterArgs,
) -> list[BufferedRequest]:
    control_buffer = SentryAppWebhookRequestsBuffer(sentry_app)

    event = filter.get("event", None)
    errors_only = filter.get("errors_only", False)

    unfiltered_requests = [
        serialize_rpc_sentry_app_request(req)
        for req in control_buffer.get_requests(event=event, errors_only=errors_only)
    ]
    return filter_requests(
        unfiltered_requests,
        datetime_org_filter,
    )