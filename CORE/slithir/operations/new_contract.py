from securewei.core.declarations.contract import Contract
from securewei.slithir.operations import Call, OperationWithLValue
from securewei.slithir.utils.utils import is_valid_lvalue, is_valid_rvalue
from securewei.slithir.variables.constant import Constant


class NewContract(Call, OperationWithLValue):

    def __init__(self, contract_name, lvalue):
        assert isinstance(contract_name, Constant)
        assert is_valid_lvalue(lvalue)
        super(NewContract, self).__init__()
        self._contract_name = contract_name
        # todo create analyze to add the contract instance
        self._lvalue = lvalue
        self._callid = None # only used if gas/value != 0
        self._call_value = None
    @property
    def call_value(self):
        return self._call_value

    @call_value.setter
    def call_value(self, v):
        self._call_value = v

    @property
    def call_id(self):
        return self._callid

    @call_id.setter
    def call_id(self, c):
        self._callid = c


    @property
    def contract_name(self):
        return self._contract_name


    @property
    def read(self):
        return list(self.arguments)
    def __str__(self):
        value = ''
        if self.call_value:
            value = 'value:{}'.format(self.call_value)
        args = [str(a) for a in self.arguments]
        return '{} = new {}({}) {}'.format(self.lvalue, self.contract_name, ','.join(args), value)
