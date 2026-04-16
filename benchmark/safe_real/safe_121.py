# source: DjangoSafe / django/forms/fields.py
# function: to_python

class BaseTemporalField:
    def to_python(self, value):
        value = value.strip()
        # Try to strptime against each input format.
        for format in self.input_formats:
            try:
                return self.strptime(value, format)
            except (ValueError, TypeError):
                continue
        raise ValidationError(self.error_messages["invalid"], code="invalid")