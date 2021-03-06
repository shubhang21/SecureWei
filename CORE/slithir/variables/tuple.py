
from securewei.core.variables.variable import Variable

class TupleVariable(Variable):

    COUNTER = 0

    def __init__(self):
        super(TupleVariable, self).__init__()
        self._index = TupleVariable.COUNTER
        TupleVariable.COUNTER += 1

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, idx):
        self._index = idx

    @property
    def name(self):
        return 'TUPLE_{}'.format(self.index)

    def __str__(self):
        return self.name
