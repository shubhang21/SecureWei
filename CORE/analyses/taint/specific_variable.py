"""
    Compute taint from a specific variable

    Do not propagate taint on protected function or constructor
    Propage to state variables
    Iterate until it finding a fixpoint
"""
from securewei.core.declarations.solidity_variables import SolidityVariable
from securewei.core.variables.state_variable import StateVariable
from securewei.core.variables.variable import Variable
from securewei.slithir.operations import Index, Member, OperationWithLValue
from securewei.slithir.variables import ReferenceVariable, TemporaryVariable

from .common import iterate_over_irs

def make_key(variable):
    if isinstance(variable, Variable):
        key = 'TAINT_{}{}{}'.format(variable.contract.name,
                                    variable.name,
                                    str(type(variable)))
    else:
        assert isinstance(variable, SolidityVariable)
        key = 'TAINT_{}{}'.format(variable.name,
                                    str(type(variable)))
    return key

def _transfer_func_with_key(ir, read, refs, taints, key):
    if isinstance(ir, OperationWithLValue) and ir.lvalue:
        if any(is_tainted_from_key(var_read, key) or var_read in taints for var_read in read):
            taints += [ir.lvalue]
            ir.lvalue.context[key] = True
            lvalue = ir.lvalue
            while  isinstance(lvalue, ReferenceVariable):
                taints += [refs[lvalue]]
                lvalue = refs[lvalue]
                lvalue.context[key] = True
    return taints

def _visit_node(node, visited, key):
    if node in visited:
        return

    visited = visited + [node]
    taints = node.function.securewei.context[key]

    # taints only increase
    # if we already see this node with the last taint set
    # we dont need to explore itœ
    if node in node.securewei.context['visited_all_paths']:
        if node.securewei.context['visited_all_paths'][node] == taints:
            return

    node.securewei.context['visited_all_paths'][node] = taints

    # use of lambda function, as the key is required for this transfer_func 
    _transfer_func_ = lambda _ir, _read, _refs, _taints: _transfer_func_with_key(_ir,
                                                                                 _read,
                                                                                 _refs,
                                                                                 _taints,
                                                                                 key)
    taints = iterate_over_irs(node.irs, _transfer_func_, taints)

    taints = [v for v in taints if not isinstance(v, (TemporaryVariable, ReferenceVariable))]

    node.function.securewei.context[key] = list(set(taints))

    for son in node.sons:
        _visit_node(son, visited, key)

def run_taint(securewei, taint):

    key = make_key(taint)

    # if a node was already visited by another path
    # we will only explore it if the traversal brings
    # new variables written
    # This speedup the exploration through a light fixpoint
    # Its particular useful on 'complex' functions with several loops and conditions
    securewei.context['visited_all_paths'] = {}

    prev_taints = []
    securewei.context[key] = [taint]
    # Loop until reaching a fixpoint
    while(set(prev_taints) != set(securewei.context[key])):
        prev_taints = securewei.context[key]
        for contract in securewei.contracts:
            for function in contract.functions:
                # Dont propagated taint on protected functions
                if function.is_implemented and not function.is_protected():
                    securewei.context[key] = list(set(securewei.context[key]))
                    _visit_node(function.entry_point, [], key)

    securewei.context[key] = [v for v in prev_taints if isinstance(v, (StateVariable, SolidityVariable))]

def is_tainted(variable, taint):
    """
    Args:
        variable (Variable)
        taint (Variable): Root of the taint
    """
    if not isinstance(variable, (Variable, SolidityVariable)):
        return False
    key = make_key(taint)
    return key in variable.context and variable.context[key]

def is_tainted_from_key(variable, key):
    """
    Args:
        variable (Variable)
        key (str): key
    """
    if not isinstance(variable, (Variable, SolidityVariable)):
        return False
    return key in variable.context and variable.context[key]


def get_state_variable_tainted(securewei, taint):
    key = make_key(taint)
    return securewei.context[key]
