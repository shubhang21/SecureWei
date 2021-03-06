import logging
from securewei.slithir.operations.lvalue import OperationWithLValue
from securewei.core.variables.variable import Variable
from securewei.slithir.utils.utils import is_valid_lvalue, is_valid_rvalue

class Push(OperationWithLValue):

    def __init__(self, array, value):
        assert is_valid_rvalue(value)
        assert is_valid_lvalue(array)
        self._value = value
        self._lvalue = array

    @property
    def read(self):
        return [self._value]

    @property
    def array(self):
        return self._lvalue

    @property
    def value(self):
        return self._value

    def __str__(self):
        return "PUSH {} in {}".format(self.value, self.lvalue)
