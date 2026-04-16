def explain(self, *args, **kwargs):
    def explain(self, using, format=None, **options):
        q = self.clone()
        q.explain_info = ExplainInfo(format, options)
        compiler = q.get_compiler(using=using)
        return "\n".join(compiler.explain_query())
