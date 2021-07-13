from securewei.core.declarations.function import Function
from securewei.core.solidity_types import FunctionType
from securewei.core.variables.variable import Variable
from securewei.slithir.operations.call import Call
from securewei.slithir.operations.lvalue import OperationWithLValue
from securewei.slithir.utils.utils import is_valid_lvalue


class InternalDynamicCall(Call, OperationWithLValue):

    def __init__(self, lvalue, function, function_type):
        assert isinstance(function_type, FunctionType)
        assert isinstance(function, Variable)
        assert is_valid_lvalue(lvalue)
        super(InternalDynamicCall, self).__init__()
        self._function = function
        self._function_type = function_type
        self._lvalue = lvalue

    @property
    def read(self):
        return list(self.arguments)

    @property
    def function(self):
        return self._function

    @property
    def function_type(self):
        return self._function_type

    def __str__(self):
        args = [str(a) for a in self.arguments]
        if not self.lvalue:
            lvalue = ''
        elif isinstance(self.lvalue.type, (list,)):
            lvalue = '{}({}) = '.format(self.lvalue, ','.join(str(x) for x in self.lvalue.type))
        else:
            lvalue = '{}({}) = '.format(self.lvalue, self.lvalue.type)
        txt = '{}INTERNAL_DYNAMIC_CALL, {}({})'
        return txt.format(lvalue,
                          self.function.name,
                          ','.join(args))

