"""
    Compute taint on call

    use taint from state_variable

    call from slithIR with a taint set to yes means its destination is tainted
"""
from securewei.analyses.taint.state_variables import get_taint as get_taint_state
from securewei.core.declarations import SolidityVariableComposed
from securewei.slithir.operations import (HighLevelCall, Index, LowLevelCall,
                                        Member, OperationWithLValue, Send,
                                        Transfer)
from securewei.slithir.variables import ReferenceVariable

from .common import iterate_over_irs

KEY = 'TAINT_CALL_DESTINATION'

def _transfer_func(ir, read, refs, taints):
    if isinstance(ir, OperationWithLValue) and any(var_read in taints for var_read in read):
        taints += [ir.lvalue]
        lvalue = ir.lvalue
        while  isinstance(lvalue, ReferenceVariable):
            taints += [refs[lvalue]]
            lvalue = refs[lvalue]
    if isinstance(ir, (HighLevelCall, LowLevelCall, Transfer, Send)):
        if ir.destination in taints:
            ir.context[KEY] = True

    return taints

def _visit_node(node, visited, taints):
    if node in visited:
        return

    visited += [node]

    taints = iterate_over_irs(node.irs, _transfer_func, taints)

    for son in node.sons:
        _visit_node(son, visited, taints)

def _run_taint(securewei, initial_taint):
    if KEY in securewei.context:
        return
    for contract in securewei.contracts:
        for function in contract.functions:
            if not function.is_implemented:
                continue
            _visit_node(function.entry_point, [], initial_taint + function.parameters)

def run_taint(securewei):
    initial_taint = get_taint_state(securewei)
    initial_taint += [SolidityVariableComposed('msg.sender')]

    if KEY not in securewei.context:
        _run_taint(securewei, initial_taint)

