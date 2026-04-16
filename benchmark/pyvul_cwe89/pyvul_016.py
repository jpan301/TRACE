def __init__(self, *args, **kwargs):
    def __init__(self, expression, delimiter, distinct=False, **extra):
        distinct = 'DISTINCT ' if distinct else ''
        super(StringAgg, self).__init__(expression, delimiter=delimiter, distinct=distinct, **extra)
