# source: DjangoSafe / django/db/models/base.py
# function: date_error_message

class Model:
    def date_error_message(self, lookup_type, field_name, unique_for):
        opts = self._meta
        field = opts.get_field(field_name)
        return ValidationError(
            message=field.error_messages["unique_for_date"],
            code="unique_for_date",
            params={
                "model": self,
                "model_name": capfirst(opts.verbose_name),
                "lookup_type": lookup_type,
                "field": field_name,
                "field_label": capfirst(field.verbose_name),
                "date_field": unique_for,
                "date_field_label": capfirst(opts.get_field(unique_for).verbose_name),
            },
        )