# source: DjangoSafe / django/http/response.py
# function: __init__

class JsonResponse:
    def __init__(
        self,
        data,
        encoder=DjangoJSONEncoder,
        safe=True,
        json_dumps_params=None,
        **kwargs,
    ):
        if safe and not isinstance(data, dict):
            raise TypeError(
                "In order to allow non-dict objects to be serialized set the "
                "safe parameter to False."
            )
        if json_dumps_params is None:
            json_dumps_params = {}
        kwargs.setdefault("content_type", "application/json")
        data = json.dumps(data, cls=encoder, **json_dumps_params)
        super().__init__(content=data, **kwargs)