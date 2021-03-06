from securewei.slithir.operations.operation import Operation

class OperationWithLValue(Operation):
    '''
        Operation with a lvalue
    '''

    def __init__(self):
        super(OperationWithLValue, self).__init__()

        self._lvalue = None

    @property
    def lvalue(self):
        return self._lvalue

    @lvalue.setter
    def lvalue(self, lvalue):
        self._lvalue = lvalue
