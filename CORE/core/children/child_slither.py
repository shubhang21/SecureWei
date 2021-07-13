
class Childsecurewei:

    def __init__(self):
        super(Childsecurewei, self).__init__()
        self._securewei = None

    def set_securewei(self, securewei):
        self._securewei = securewei

    @property
    def securewei(self):
        return self._securewei
