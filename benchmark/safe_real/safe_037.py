# source: SentrySafe / src/sentry/seer/anomaly_detection/store_data_workflow_engine.py
# function: handle_send_historical_data_to_seer

def handle_send_historical_data_to_seer(
    detector: Detector,
    data_source: DataSource,
    data_condition: DataCondition,
    snuba_query: SnubaQuery,
    project: Project,
    method: str,
    event_types: list[SnubaQueryEventType.EventType] | None = None,
) -> None:
    event_types_param = event_types or snuba_query.event_types
    try:
        send_historical_data_to_seer(
            detector=detector,
            data_source=data_source,
            data_condition=data_condition,
            project=project,
            snuba_query=snuba_query,
            event_types=event_types_param,
        )
    except (TimeoutError, MaxRetryError):
        raise TimeoutError(f"Failed to send data to Seer - cannot {method} detector.")
    except ParseError:
        raise ParseError("Failed to parse Seer store data response")
    except ValidationError:
        raise ValidationError(f"Failed to send data to Seer - cannot {method} detector.")
    except Exception as e:
        sentry_sdk.capture_exception(e)
        raise ValidationError(f"Failed to send data to Seer - cannot {method} detector.")