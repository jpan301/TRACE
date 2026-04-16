def explain_query_prefix(self, *args, **kwargs):
    def explain_query_prefix(self, format=None, **options):
        prefix = super().explain_query_prefix(format)
        extra = {}
        if format:
            extra['FORMAT'] = format
        if options:
            extra.update({
                name.upper(): 'true' if value else 'false'
                for name, value in options.items()
            })
        if extra:
            prefix += ' (%s)' % ', '.join('%s %s' % i for i in extra.items())
        return prefix
