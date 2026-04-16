# source: DjangoSafe / django/contrib/admin/checks.py
# function: _check_exclude

class BaseModelAdminChecks:
    def _check_exclude(self, obj):
        """Check that exclude is a sequence without duplicates."""

        if obj.exclude is None:  # default value is None
            return []
        elif not isinstance(obj.exclude, (list, tuple)):
            return must_be(
                "a list or tuple", option="exclude", obj=obj, id="admin.E014"
            )
        field_counts = collections.Counter(obj.exclude)
        if duplicate_fields := [
            field for field, count in field_counts.items() if count > 1
        ]:
            return [
                checks.Error(
                    "The value of 'exclude' contains duplicate field(s).",
                    hint="Remove duplicates of %s."
                    % ", ".join(map(repr, duplicate_fields)),
                    obj=obj.__class__,
                    id="admin.E015",
                )
            ]
        else:
            return []