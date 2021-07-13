import abc
import re

from securewei.utils.colors import green, yellow, red
from securewei.detectors.reentrancy.reentrancy import Reentrancy


class IncorrectDetectorInitialization(Exception):
    pass


class DetectorClassification:
    HIGH = 0
    MEDIUM = 1
    LOW = 2
    INFORMATIONAL = 3


classification_colors = {
    DetectorClassification.INFORMATIONAL: green,
    DetectorClassification.LOW: green,
    DetectorClassification.MEDIUM: yellow,
    DetectorClassification.HIGH: red,
}

classification_txt = {
    DetectorClassification.INFORMATIONAL: 'Informational',
    DetectorClassification.LOW: 'Low',
    DetectorClassification.MEDIUM: 'Medium',
    DetectorClassification.HIGH: 'High',
}

class AbstractDetector(metaclass=abc.ABCMeta):
    ARGUMENT = ''  # run the detector with securewei.py --ARGUMENT
    HELP = ''  # help information
    IMPACT = None
    CONFIDENCE = None

    def __init__(self, securewei, logger, args=None):
        self.securewei = securewei
        self.contracts = securewei.contracts
        self.filename = args.filename
        self.logger = logger

        if not self.HELP:
            raise IncorrectDetectorInitialization('HELP is not initialized {}'.format(self.__class__.__name__))

        if not self.ARGUMENT:
            raise IncorrectDetectorInitialization('ARGUMENT is not initialized {}'.format(self.__class__.__name__))

        if re.match('^[a-zA-Z0-9_-]*$', self.ARGUMENT) is None:
            raise IncorrectDetectorInitialization('ARGUMENT has illegal character {}'.format(self.__class__.__name__))

        if self.IMPACT not in [DetectorClassification.LOW,
                                       DetectorClassification.MEDIUM,
                                       DetectorClassification.HIGH,
                                       DetectorClassification.INFORMATIONAL]:
            raise IncorrectDetectorInitialization('IMPACT is not initialized {}'.format(self.__class__.__name__))

        if self.CONFIDENCE not in [DetectorClassification.LOW,
                                       DetectorClassification.MEDIUM,
                                       DetectorClassification.HIGH,
                                       DetectorClassification.INFORMATIONAL]:
            raise IncorrectDetectorInitialization('CONFIDENCE is not initialized {}'.format(self.__class__.__name__))

    def log(self, info):
        if self.logger:
            info = " "+info
            self.logger.info(self.color(info))

    @abc.abstractmethod
    def detect(self):
        """TODO Documentation"""
        print('detecting')
        return

    @property
    def color(self):
        return classification_colors[self.IMPACT]


    result=Reentrancy.detect()
    print(result)