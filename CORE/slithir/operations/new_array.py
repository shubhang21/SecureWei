from securewei.slithir.operations.lvalue import OperationWithLValue
from securewei.slithir.operations.call import Call
from securewei.core.solidity_types.type import Type

class NewArray(Call, OperationWithLValue):

    def __init__(self, depth, array_type, lvalue):
        super(NewArray, self).__init__()
        assert isinstance(array_type, Type)
        self._depth = depth
        self._array_type = array_type

        self._lvalue = lvalue

    @property
    def array_type(self):
        return self._array_type

    @property
    def read(self):
        return list(self.arguments)

    @property
    def depth(self):
        return self._depth

    def __str__(self):
        args = [str(a) for a in self.arguments]
        return '{} = new {}{}({})'.format(self.lvalue, self.array_type, '[]'*self.depth, ','.join(args))
