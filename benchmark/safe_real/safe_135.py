# source: SentrySafe / src/sentry/testutils/helpers/link_header.py
# function: parse_link_header

def parse_link_header(instr: str) -> dict[str, dict[str, str | None]]:
    """
    Given a link-value (i.e., after separating the header-value on commas),
    return a dictionary whose keys are link URLs and values are dictionaries
    of the parameters for their associated links.

    Note that internationalised parameters (e.g., title*) are
    NOT percent-decoded.

    Also, only the last instance of a given parameter will be included.

    For example,

    >>> parse_link_value('</foo>; rel="self"; title*=utf-8\'de\'letztes%20Kapitel')
    {'/foo': {'title*': "utf-8'de'letztes%20Kapitel", 'rel': 'self'}}

    """
    out: dict[str, dict[str, str | None]] = {}
    if not instr:
        return out

    for link in [h.strip() for h in link_splitter.findall(instr)]:
        url, params = link.split(">", 1)
        url = url[1:]
        param_dict: dict[str, str | None] = {}
        for param in _splitstring(params, PARAMETER, r"\s*;\s*"):
            try:
                a, v = param.split("=", 1)
                param_dict[a.lower()] = _unquotestring(v)
            except ValueError:
                param_dict[param.lower()] = None
        out[url] = param_dict
    return out