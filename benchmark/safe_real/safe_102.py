# source: DjangoSafe / django/core/checks/translation.py
# function: check_setting_languages

def check_setting_languages(app_configs, **kwargs):
    """Error if LANGUAGES setting is invalid."""
    return [
        Error(E002.msg.format(tag), id=E002.id)
        for tag, _ in settings.LANGUAGES
        if not isinstance(tag, str) or not language_code_re.match(tag)
    ]