# source: SentrySafe / src/sentry/issue_detection/detectors/query_injection_detector.py
# function: _is_span_eligible

class QueryInjectionDetector:
    def _is_span_eligible(self, span: Span) -> bool:
        if not span.get("span_id"):
            return False

        op = span.get("op", None)

        if not op or not op.startswith("db") or op.startswith("db.redis"):
            return False

        description = span.get("description", None)

        if not description:
            return False

        sql_keywords = ("SELECT", "UPDATE", "INSERT")
        if any(description.upper().startswith(keyword) for keyword in sql_keywords):
            return False

        return True