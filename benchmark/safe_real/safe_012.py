# source: DjangoSafe / django/contrib/postgres/fields/hstore.py
# function: validate

class HStoreField:
    def validate(self, value, model_instance):
        super().validate(value, model_instance)
        for key, val in value.items():
            if not isinstance(val, str) and val is not None:
                raise exceptions.ValidationError(
                    self.error_messages["not_a_string"],
                    code="not_a_string",
                    params={"key": key},
                )