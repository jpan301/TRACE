# source: DjangoSafe / django/forms/forms.py
# function: add_prefix

class BaseForm:
    def add_prefix(self, field_name):
        """
        Return the field name with a prefix appended, if this Form has a
        prefix set.

        Subclasses may wish to override.
        """
        return "%s-%s" % (self.prefix, field_name) if self.prefix else field_name