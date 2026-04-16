def add_annotation(self, *args, **kwargs):
    def add_annotation(self, annotation, alias, is_summary=False):
        """Add a single annotation expression to the Query."""
        annotation = annotation.resolve_expression(self, allow_joins=True, reuse=None,
                                                   summarize=is_summary)
        self.append_annotation_mask([alias])
        self.annotations[alias] = annotation
