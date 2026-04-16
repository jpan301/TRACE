# source: DjangoSafe / django/template/library.py
# function: dec

class Library:
        def dec(func):
            with lazy_annotations():
                (
                    params,
                    varargs,
                    varkw,
                    defaults,
                    kwonly,
                    kwonly_defaults,
                    _,
                ) = getfullargspec(unwrap(func))
            function_name = name or func.__name__

            if takes_context:
                if params and params[0] == "context":
                    del params[0]
                else:
                    raise TemplateSyntaxError(
                        f"{function_name!r} is decorated with takes_context=True so it "
                        "must have a first argument of 'context'"
                    )

            @wraps(func)
            def compile_func(parser, token):
                bits = token.split_contents()[1:]
                target_var = None
                if len(bits) >= 2 and bits[-2] == "as":
                    target_var = bits[-1]
                    bits = bits[:-2]
                args, kwargs = parse_bits(
                    parser,
                    bits,
                    params,
                    varargs,
                    varkw,
                    defaults,
                    kwonly,
                    kwonly_defaults,
                    function_name,
                )
                return SimpleNode(func, takes_context, args, kwargs, target_var)

            self.tag(function_name, compile_func)
            return func