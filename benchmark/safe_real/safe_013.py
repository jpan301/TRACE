# source: DjangoSafe / django/template/defaulttags.py
# function: verbatim

def verbatim(parser, token):
    """
    Stop the template engine from rendering the contents of this block tag.

    Usage::

        {% verbatim %}
            {% don't process this %}
        {% endverbatim %}

    You can also designate a specific closing tag block (allowing the
    unrendered use of ``{% endverbatim %}``)::

        {% verbatim myblock %}
            ...
        {% endverbatim myblock %}
    """
    nodelist = parser.parse(("endverbatim",))
    parser.delete_first_token()
    return VerbatimNode(nodelist.render(Context()))