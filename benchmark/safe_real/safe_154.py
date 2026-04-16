# source: DjangoSafe / django/contrib/admin/options.py
# function: log_change

class ModelAdmin:
    def log_change(self, request, obj, message):
        """
        Log that an object has been successfully changed.

        The default implementation creates an admin LogEntry object.
        """
        from django.contrib.admin.models import CHANGE, LogEntry

        return LogEntry.objects.log_actions(
            user_id=request.user.pk,
            queryset=[obj],
            action_flag=CHANGE,
            change_message=message,
            single_object=True,
        )