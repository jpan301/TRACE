# source: SentrySafe / src/sentry/sentry_apps/services/app/impl.py
# function: serialize_many

class DatabaseBackedAppService:
    def serialize_many(
        self,
        *,
        filter: SentryAppInstallationFilterArgs,
        as_user: RpcUser | None = None,
        auth_context: AuthenticationContext | None = None,
    ) -> list[OpaqueSerializedResponse]:
        return self._FQ.serialize_many(filter, as_user, auth_context)