# source: SentrySafe / src/sentry/api/serializers/models/project.py
# function: serialize

class ProjectSerializer:
    def serialize(
        self,
        obj: Project,
        attrs: Mapping[str, Any],
        user: User | RpcUser | AnonymousUser,
        **kwargs: Any,
    ) -> ProjectSerializerResponse:
        status_label = STATUS_LABELS.get(obj.status, "unknown")

        context: ProjectSerializerResponse = {
            "id": str(obj.id),
            "slug": obj.slug,
            "name": obj.name,  # Deprecated
            "platform": obj.platform,
            "dateCreated": obj.date_added,
            "isBookmarked": attrs["is_bookmarked"],
            "isMember": attrs["is_member"],
            "features": attrs["features"],
            "firstEvent": obj.first_event,
            "firstTransactionEvent": bool(obj.flags.has_transactions),
            "access": attrs["access"],
            "hasAccess": attrs["has_access"],
            "hasMinifiedStackTrace": bool(obj.flags.has_minified_stack_trace),
            "hasMonitors": bool(obj.flags.has_cron_monitors),
            "hasProfiles": bool(obj.flags.has_profiles),
            "hasReplays": bool(obj.flags.has_replays),
            "hasFeedbacks": bool(obj.flags.has_feedbacks),
            "hasFlags": bool(obj.flags.has_flags),
            "hasNewFeedbacks": bool(obj.flags.has_new_feedbacks),
            "hasSessions": bool(obj.flags.has_sessions),
            # whether first span has been sent for each insight module
            "hasInsightsHttp": bool(obj.flags.has_insights_http),
            "hasInsightsDb": bool(obj.flags.has_insights_db),
            "hasInsightsAssets": bool(obj.flags.has_insights_assets),
            "hasInsightsAppStart": bool(obj.flags.has_insights_app_start),
            "hasInsightsScreenLoad": bool(obj.flags.has_insights_screen_load),
            "hasInsightsVitals": bool(obj.flags.has_insights_vitals),
            "hasInsightsCaches": bool(obj.flags.has_insights_caches),
            "hasInsightsQueues": bool(obj.flags.has_insights_queues),
            "hasInsightsAgentMonitoring": bool(obj.flags.has_insights_agent_monitoring),
            "hasInsightsMCP": bool(obj.flags.has_insights_mcp),
            "hasLogs": get_has_logs(obj),
            "hasTraceMetrics": get_has_trace_metrics(obj),
            "isInternal": obj.is_internal_project(),
            "isPublic": obj.public,
            # Projects don't have avatar uploads, but we need to maintain the payload shape for
            # compatibility.
            "avatar": {"avatarType": "letter_avatar", "avatarUuid": None},
            "color": obj.color,
            "status": status_label,
        }
        if "stats" in attrs:
            context["stats"] = attrs["stats"]
        if "transactionStats" in attrs:
            context["transactionStats"] = attrs["transactionStats"]
        if "sessionStats" in attrs:
            context["sessionStats"] = attrs["sessionStats"]
        return context