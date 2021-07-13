import logging
from securewei.slithir.operations.lvalue import OperationWithLValue
from securewei.slithir.variables.tuple import TupleVariable

from securewei.slithir.utils.utils import is_valid_lvalue, is_valid_rvalue

class Unpack(OperationWithLValue):

    def __init__(self, result, tuple_var, idx):
        assert is_valid_lvalue(result)
        assert isinstance(tuple_var, TupleVariable)
        assert isinstance(idx, int)
        super(Unpack, self).__init__()
        self._tuple = tuple_var
        self._idx = idx
        self._lvalue = result

    @property
    def read(self):
        return [self.tuple]

    @property
    def tuple(self):
        return self._tuple

    @property
    def index(self):
        return self._idx

    def __str__(self):
        return "{} = UNPACK {} index: {} ".format(self.lvalue, self.tuple, self.index)
