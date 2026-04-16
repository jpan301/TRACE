# source: SentrySafe / src/sentry/issues/escalating/forecasts.py
# function: generate_and_save_forecasts

def generate_and_save_forecasts(groups: Iterable[Group]) -> None:
    """
    Generates and saves a list of forecasted values for each group.
    `groups`: Sequence of groups to be forecasted
    """
    groups = [group for group in groups if group.issue_type.should_detect_escalation()]
    past_counts = query_groups_past_counts(groups)
    group_counts = parse_groups_past_counts(past_counts)
    save_forecast_per_group(groups, group_counts)
    logger.info(
        "generate_and_save_forecasts",
        extra={
            "detail": "Created forecast for groups",
            "group_ids": [group.id for group in groups],
        },
    )