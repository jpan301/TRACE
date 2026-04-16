def add_annotation(self, *args, **kwargs):
    def add_annotation(self, annotation, alias, is_summary=False, select=True):
        """Add a single annotation expression to the Query."""
        annotation = annotation.resolve_expression(
            self, allow_joins=True, reuse=None, summarize=is_summary
        )
        if select:
            self.append_annotation_mask([alias])
        else:
            self.set_annotation_mask(set(self.annotation_select).difference({alias}))
        self.annotations[alias] = annotation
