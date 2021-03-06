from securewei.core.cfg.node import Node
from securewei.core.cfg.node import NodeType
from securewei.solc_parsing.expressions.expression_parsing import parse_expression
from securewei.visitors.expression.read_var import ReadVar
from securewei.visitors.expression.write_var import WriteVar
from securewei.visitors.expression.find_calls import FindCalls

from securewei.visitors.expression.export_values import ExportValues
from securewei.core.declarations.solidity_variables import SolidityVariable, SolidityFunction
from securewei.core.declarations.function import Function

from securewei.core.variables.state_variable import StateVariable

from securewei.core.expressions.identifier import Identifier
from securewei.core.expressions.assignment_operation import AssignmentOperation, AssignmentOperationType

class NodeSolc(Node):

    def __init__(self, nodeType, nodeId):
        super(NodeSolc, self).__init__(nodeType, nodeId)
        self._unparsed_expression = None

    def add_unparsed_expression(self, expression):
        assert self._unparsed_expression is None
        self._unparsed_expression = expression

    def analyze_expressions(self, caller_context):
        if self.type == NodeType.VARIABLE and not self._expression:
            self._expression = self.variable_declaration.expression
        if self._unparsed_expression:
            expression = parse_expression(self._unparsed_expression, caller_context)
            self._expression = expression
            self._unparsed_expression = None

        if self.expression:

            if self.type == NodeType.VARIABLE:
                # Update the expression to be an assignement to the variable
                #print(self.variable_declaration)
                self._expression = AssignmentOperation(Identifier(self.variable_declaration),
                                                       self.expression,
                                                       AssignmentOperationType.ASSIGN,
                                                       self.variable_declaration.type)

            expression = self.expression
            pp = ReadVar(expression)
            self._expression_vars_read = pp.result()
            vars_read = [ExportValues(v).result() for v in self._expression_vars_read]
            self._vars_read = [item for sublist in vars_read for item in sublist]
            self._state_vars_read = [x for x in self.variables_read if\
                                     isinstance(x, (StateVariable))]
            self._solidity_vars_read = [x for x in self.variables_read if\
                                        isinstance(x, (SolidityVariable))]

            pp = WriteVar(expression)
            self._expression_vars_written = pp.result()
            vars_written = [ExportValues(v).result() for v in self._expression_vars_written]
            self._vars_written = [item for sublist in vars_written for item in sublist]
            self._state_vars_written = [x for x in self.variables_written if\
                                        isinstance(x, StateVariable)]

            pp = FindCalls(expression)
            self._expression_calls = pp.result()
            calls = [ExportValues(c).result() for c in self.calls_as_expression]
            calls = [item for sublist in calls for item in sublist]
            self._internal_calls = [c for c in calls if isinstance(c, (Function, SolidityFunction))]

            self._external_calls = [c for c in self.calls_as_expression if not isinstance(c.called, Identifier)]

