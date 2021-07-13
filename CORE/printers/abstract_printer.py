import abc


class IncorrectPrinterInitialization(Exception):
    pass


class AbstractPrinter(metaclass=abc.ABCMeta):
    ARGUMENT = ''  # run the printer with securewei.py --ARGUMENT
    HELP = ''  # help information

    def __init__(self, securewei, logger):
        self.securewei = securewei
        self.contracts = securewei.contracts
        self.filename = securewei.filename
        self.logger = logger

        if not self.HELP:
            raise IncorrectPrinterInitialization('HELP is not initialized')

        if not self.ARGUMENT:
            raise IncorrectPrinterInitialization('ARGUMENT is not initialized')

    def info(self, info):
        if self.logger:
            self.logger.info(info)

    @abc.abstractmethod
    def output(self, filename):
        """TODO Documentation"""
        return
