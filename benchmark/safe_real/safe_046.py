# source: DjangoSafe / django/contrib/auth/views.py
# function: redirect_to_login

def redirect_to_login(next, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Redirect the user to the login page, passing the given 'next' page.
    """
    resolved_url = resolve_url(login_url or settings.LOGIN_URL)

    login_url_parts = list(urlsplit(resolved_url))
    if redirect_field_name:
        querystring = QueryDict(login_url_parts[3], mutable=True)
        querystring[redirect_field_name] = next
        login_url_parts[3] = querystring.urlencode(safe="/")

    return HttpResponseRedirect(urlunsplit(login_url_parts))