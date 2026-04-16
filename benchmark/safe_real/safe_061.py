# source: DjangoSafe / django/urls/base.py
# function: translate_url

def translate_url(url, lang_code):
    """
    Given a URL (absolute or relative), try to get its translated version in
    the `lang_code` language (either by i18n_patterns or by translated regex).
    Return the original URL if no translated version is found.
    """
    parsed = urlsplit(url)
    try:
        # URL may be encoded.
        match = resolve(unquote(parsed.path))
    except Resolver404:
        pass
    else:
        to_be_reversed = (
            "%s:%s" % (match.namespace, match.url_name)
            if match.namespace
            else match.url_name
        )
        with override(lang_code):
            try:
                url = reverse(to_be_reversed, args=match.args, kwargs=match.kwargs)
            except NoReverseMatch:
                pass
            else:
                url = urlunsplit(
                    (parsed.scheme, parsed.netloc, url, parsed.query, parsed.fragment)
                )
    return url