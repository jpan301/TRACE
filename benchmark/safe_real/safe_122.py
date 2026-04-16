# source: DjangoSafe / django/views/defaults.py
# function: bad_request

def bad_request(request, exception, template_name=ERROR_400_TEMPLATE_NAME):
    """
    400 error handler.

    Templates: :template:`400.html`
    Context: None
    """
    try:
        template = loader.get_template(template_name)
        body = template.render(request=request)
    except TemplateDoesNotExist:
        if template_name != ERROR_400_TEMPLATE_NAME:
            # Reraise if it's a missing custom template.
            raise
        return HttpResponseBadRequest(
            ERROR_PAGE_TEMPLATE % {"title": "Bad Request (400)", "details": ""},
        )
    # No exception content is passed to the template, to not disclose any
    # sensitive information.
    return HttpResponseBadRequest(body)