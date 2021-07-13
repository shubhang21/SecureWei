from securewei.core.variables.local_variable import LocalVariable
from securewei.core.variables.state_variable import StateVariable

from securewei.core.declarations.solidity_variables import SolidityVariable

from securewei.slithir.variables.temporary import TemporaryVariable
from securewei.slithir.variables.constant import Constant
from securewei.slithir.variables.reference import ReferenceVariable
from securewei.slithir.variables.tuple import TupleVariable

def is_valid_rvalue(v):
    return isinstance(v, (StateVariable, LocalVariable, TemporaryVariable, Constant, SolidityVariable, ReferenceVariable))

def is_valid_lvalue(v):
    return isinstance(v, (StateVariable, LocalVariable, TemporaryVariable, ReferenceVariable, TupleVariable))

