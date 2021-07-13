"""
    Compute taint on state variables

    Do not propagate taint on protected function
    Compute taint from function parameters, msg.sender and msg.value
    Iterate until it finding a fixpoint

"""
from securewei.core.declarations.solidity_variables import \
    SolidityVariableComposed
from securewei.core.variables.state_variable import StateVariable
from securewei.slithir.operations import Index, Member, OperationWithLValue
from securewei.slithir.variables import ReferenceVariable, TemporaryVariable

from .common import iterate_over_irs
KEY = 'TAINT_STATE_VARIABLES'

def _transfer_func(ir, read, refs, taints):
    if isinstance(ir, OperationWithLValue) and any(var_read in taints for var_read in read):
        taints += [ir.lvalue]
        lvalue = ir.lvalue
        while  isinstance(lvalue, ReferenceVariable):
            taints += [refs[lvalue]]
            lvalue = refs[lvalue]
    return taints

def _visit_node(node, visited):
    if node in visited:
        return

    visited += [node]
    taints = node.function.securewei.context[KEY]

    taints = iterate_over_irs(node.irs, _transfer_func, taints)

    taints = [v for v in taints if not isinstance(v, (TemporaryVariable, ReferenceVariable))]

    node.function.securewei.context[KEY] = list(set(taints))

    for son in node.sons:
        _visit_node(son, visited)


def _run_taint(securewei, initial_taint):
    if KEY in securewei.context:
        return

    prev_taints = []
    securewei.context[KEY] = initial_taint
    # Loop until reaching a fixpoint
    while(set(prev_taints) != set(securewei.context[KEY])):
        prev_taints = securewei.context[KEY]
        for contract in securewei.contracts:
            for function in contract.functions:
                if not function.is_implemented:
                    continue
                # Dont propagated taint on protected functions
                if not function.is_protected():
                    securewei.context[KEY] = list(set(securewei.context[KEY] + function.parameters))
                    _visit_node(function.entry_point, [])

    securewei.context[KEY] = [v for v in prev_taints if isinstance(v, StateVariable)]

def run_taint(securewei, initial_taint=None):
    if initial_taint is None:
        initial_taint = [SolidityVariableComposed('msg.sender')]
        initial_taint += [SolidityVariableComposed('msg.value')]

    if KEY not in securewei.context:
        _run_taint(securewei, initial_taint)

def get_taint(securewei, initial_taint=None):
    """
        Return the state variables tainted
    Args:
        securewei:
        initial_taint (List Variable)
    Returns:
        List(StateVariable)
    """
    run_taint(securewei, initial_taint)
    return securewei.context[KEY]
