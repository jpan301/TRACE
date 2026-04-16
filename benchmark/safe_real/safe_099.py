# source: DjangoSafe / django/core/mail/__init__.py
# function: _send_server_message

def _send_server_message(
    *,
    setting_name,
    subject,
    message,
    html_message=None,
    fail_silently=False,
    connection=None,
):
    if connection is not None and fail_silently:
        raise TypeError(
            "fail_silently cannot be used with a connection. "
            "Pass fail_silently to get_connection() instead."
        )
    recipients = getattr(settings, setting_name)
    if not recipients:
        return

    # RemovedInDjango70Warning.
    if all(isinstance(a, (list, tuple)) and len(a) == 2 for a in recipients):
        warnings.warn(
            f"Using (name, address) pairs in the {setting_name} setting is deprecated."
            " Replace with a list of email address strings.",
            RemovedInDjango70Warning,
            stacklevel=2,
        )
        recipients = [a[1] for a in recipients]

    if not isinstance(recipients, (list, tuple)) or not all(
        isinstance(address, (str, Promise)) for address in recipients
    ):
        raise ImproperlyConfigured(
            f"The {setting_name} setting must be a list of email address strings."
        )

    mail = EmailMultiAlternatives(
        subject="%s%s" % (settings.EMAIL_SUBJECT_PREFIX, subject),
        body=message,
        from_email=settings.SERVER_EMAIL,
        to=recipients,
        connection=connection,
    )
    if html_message:
        mail.attach_alternative(html_message, "text/html")
    mail.send(fail_silently=fail_silently)