def as_sql(self, *args, **kwargs):
    def as_sql(self, compiler, connection):
        lhs, params = compiler.compile(self.lhs)
        return "(%s -> '%s')" % (lhs, self.key_name), params
