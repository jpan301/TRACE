# source: DjangoSafe / django/contrib/admin/checks.py
# function: _check_readonly_fields_item

class BaseModelAdminChecks:
    def _check_readonly_fields_item(self, obj, field_name, label):
        if callable(field_name):
            return []
        elif hasattr(obj, field_name):
            return []
        elif hasattr(obj.model, field_name):
            return []
        else:
            try:
                obj.model._meta.get_field(field_name)
            except FieldDoesNotExist:
                return [
                    checks.Error(
                        "The value of '%s' refers to '%s', which is not a callable, "
                        "an attribute of '%s', or an attribute of '%s'."
                        % (
                            label,
                            field_name,
                            obj.__class__.__name__,
                            obj.model._meta.label,
                        ),
                        obj=obj.__class__,
                        id="admin.E035",
                    )
                ]
            else:
                return []