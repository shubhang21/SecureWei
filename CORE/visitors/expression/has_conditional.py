
from securewei.visitors.expression.expression import ExpressionVisitor

class HasConditional(ExpressionVisitor):

    def result(self):
        # == True, to convert None to false
        return self._result is True

    def _post_conditional_expression(self, expression):
#        if self._result is True:
#            raise('securewei does not support nested ternary operator')
        self._result = True
