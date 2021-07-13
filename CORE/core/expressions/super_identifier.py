from securewei.core.expressions.expression_typed import ExpressionTyped
from securewei.core.expressions.identifier import Identifier

class SuperIdentifier(Identifier):

    def __str__(self):
        return 'super.' + str(self._value)

