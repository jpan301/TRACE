# source: PyPikaSafe / pypika/terms.py
# function: get_sql

class ComplexCriterion:
    def get_sql(self, subcriterion: bool = False, **kwargs: Any) -> str:
        sql = "{left} {comparator} {right}".format(
            comparator=self.comparator.value,
            left=self.left.get_sql(subcriterion=self.needs_brackets(self.left), **kwargs),
            right=self.right.get_sql(subcriterion=self.needs_brackets(self.right), **kwargs),
        )

        if subcriterion:
            return "({criterion})".format(criterion=sql)

        return sql