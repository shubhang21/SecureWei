import logging
from securewei.slithir.operations.lvalue import OperationWithLValue
from securewei.core.variables.variable import Variable

from securewei.slithir.utils.utils import is_valid_lvalue
class Delete(OperationWithLValue):
    """
        Delete has a lvalue, as it has for effect to change the value
        of its operand
    """

    def __init__(self, variable):
        assert is_valid_lvalue(variable)
        super(Delete, self).__init__()
        self._variable = variable
        self._lvalue = variable

    @property
    def read(self):
        return [self.variable]

    @property
    def variable(self):
        return self._variable

    def __str__(self):
        return "{} = delete {} ".format(self.lvalue, self.variable)
