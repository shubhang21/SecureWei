"""
    We use protected member, to avoid having setter in the expression
    as they should be immutable
"""
import copy
from securewei.core.expressions.assignment_operation import AssignmentOperation
from securewei.core.expressions.binary_operation import BinaryOperation
from securewei.core.expressions.call_expression import CallExpression
from securewei.core.expressions.conditional_expression import ConditionalExpression
from securewei.core.expressions.elementary_type_name_expression import ElementaryTypeNameExpression
from securewei.core.expressions.identifier import Identifier
from securewei.core.expressions.index_access import IndexAccess
from securewei.core.expressions.literal import Literal
from securewei.core.expressions.member_access import MemberAccess
from securewei.core.expressions.new_array import NewArray
from securewei.core.expressions.new_contract import NewContract
from securewei.core.expressions.new_elementary_type import NewElementaryType
from securewei.core.expressions.tuple_expression import TupleExpression
from securewei.core.expressions.type_conversion import TypeConversion
from securewei.core.expressions.unary_operation import UnaryOperation

def f_expressions(e, x):
    e._expressions.append(x)

def f_call(e, x):
    e._arguments.append(x)

def f_expression(e, x):
    e._expression = x

class SplitTernaryExpression(object):

    def __init__(self, expression):

    #    print(expression)

        if isinstance(expression, ConditionalExpression):
            self.true_expression = copy.copy(expression.then_expression)
            self.false_expression = copy.copy(expression.else_expression)
            self.condition = copy.copy(expression.if_expression)
        else:
            self.true_expression = copy.copy(expression)
            self.false_expression = copy.copy(expression)
            self.condition = None
            self.copy_expression(expression, self.true_expression, self.false_expression)

    def apply_copy(self, next_expr, true_expression, false_expression, f):

        if isinstance(next_expr, ConditionalExpression):
            f(true_expression, copy.copy(next_expr.then_expression))
            f(false_expression, copy.copy(next_expr.else_expression))
            self.condition = copy.copy(next_expr.if_expression)
            return False
        else:
            f(true_expression, copy.copy(next_expr))
            f(false_expression, copy.copy(next_expr))
            return True

    def copy_expression(self, expression, true_expression, false_expression):
            if self.condition:
                return

            if isinstance(expression, ConditionalExpression):
               raise Exception('Nested ternary operator not handled')

            if isinstance(expression, (Literal, Identifier, IndexAccess, MemberAccess)):
                return None

            elif isinstance(expression, (AssignmentOperation, BinaryOperation, TupleExpression)):
                true_expression._expressions = []
                false_expression._expressions = []

                for next_expr in expression.expressions:
                    if self.apply_copy(next_expr, true_expression, false_expression, f_expressions):
                        # always on last arguments added
                        self.copy_expression(next_expr, true_expression.expressions[-1], false_expression.expressions[-1])

            elif isinstance(expression, CallExpression):
                next_expr = expression.called
                true_expression._called = copy.copy(next_expr)
                false_expression._called = copy.copy(next_expr)

                true_expression._arguments = []
                false_expression._arguments = []

                for next_expr in expression.arguments:
                    if self.apply_copy(next_expr, true_expression, false_expression, f_call):
                        # always on last arguments added
                        self.copy_expression(next_expr, true_expression.arguments[-1], false_expression.arguments[-1])

            elif isinstance(expression, TypeConversion):
                next_expr = expression.expression
                if self.apply_copy(next_expr, true_expression, false_expression, f_expression):
                    self.copy_expression(expression.expression, true_expression.expression, false_expression.expression)

            else:
                raise Exception('Ternary operation not handled {}'.format(type(expression)))

