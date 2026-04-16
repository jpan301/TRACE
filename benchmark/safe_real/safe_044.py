# source: PyPikaSafe / pypika/queries.py
# function: using

class Joiner:
    def using(self, *fields: Any) -> QB:
        if not fields:
            raise JoinException("Parameter 'fields' is required when joining with a using clause but was not supplied.")

        self.query.do_join(JoinUsing(self.item, self.how, [Field(field) for field in fields]))
        return self.query