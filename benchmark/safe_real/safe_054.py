# source: DjangoSafe / django/core/checks/model_checks.py
# function: default_error

class DummyClass:
    def default_error(model_key, func, args, keywords):
        error_msg = (
            "%(op)s contains a lazy reference to %(model)s, but %(model_error)s."
        )
        params = {
            "op": func,
            "model": ".".join(model_key),
            "model_error": app_model_error(model_key),
        }
        return Error(error_msg % params, obj=func, id="models.E022")