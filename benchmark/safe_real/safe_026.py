# source: PyPikaSafe / pypika/terms.py
# function: right_needs_parens

class ArithmeticExpression:
    def right_needs_parens(self, curr_op, right_op) -> bool:
        """
        Returns true if the expression on the right of the current operator needs to be enclosed in parentheses.

        :param current_op:
            The current operator.
        :param right_op:
            The highest level operator of the right expression.
        """
        if right_op is None:
            # If the right expression is a single item.
            return False
        if curr_op == Arithmetic.add:
            return False
        if curr_op == Arithmetic.div:
            return True
        # The current operator is '*' or '-. If the right operator is '+' or '-', we need to add parentheses:
        # e.g. ... - (A + B), ... - (A - B)
        # Otherwise, no parentheses are necessary:
        # e.g. ... - A / B, ... - A * B
        return right_op in self.add_order