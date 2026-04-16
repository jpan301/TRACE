# source: SentrySafe / src/sentry/backup/services/import_export/impl.py
# function: get_all_globally_privileged_users

class UniversalImportExportService:
    def get_all_globally_privileged_users(self) -> set[int]:
        admin_user_pks: set[int] = set()
        admin_user_pks.update(
            User.objects.filter(Q(is_staff=True) | Q(is_superuser=True)).values_list(
                "id", flat=True
            )
        )
        admin_user_pks.update(UserPermission.objects.values_list("user_id", flat=True))
        admin_user_pks.update(UserRoleUser.objects.values_list("user_id", flat=True))
        return admin_user_pks