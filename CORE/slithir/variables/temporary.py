
from securewei.core.variables.variable import Variable
from securewei.core.children.child_node import ChildNode

class TemporaryVariable(ChildNode, Variable):

    COUNTER = 0

    def __init__(self):
        super(TemporaryVariable, self).__init__()
        self._index = TemporaryVariable.COUNTER
        TemporaryVariable.COUNTER += 1

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, idx):
        self._index = idx

    @property
    def name(self):
        return 'TMP_{}'.format(self.index)

    def __str__(self):
        return self.name
