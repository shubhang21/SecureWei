from securewei.detectors.abstract_detector import AbstractDetector, DetectorClassification


class Backdoor(AbstractDetector):
    """
    Detect function named backdoor
    """

    ARGUMENT = 'backdoor'  # securewei will launch the detector with securewei.py --mydetector
    HELP = 'function named backdoor (detector example)'
    IMPACT = DetectorClassification.HIGH
    CONFIDENCE = DetectorClassification.HIGH

    def detect(self):
        ret = []

        for contract in self.securewei.contracts_derived:
            # Check if a function has 'backdoor' in its name
            for f in contract.functions:
                if 'backdoor' in f.name:
                    # Info to be printed
                    info = 'Backdoor function found in {}.{}'.format(contract.name, f.name)
                    # Print the info
                    self.log(info)
                    # Add the result in ret
                    source = f.source_mapping
                    ret.append({'vuln': 'backdoor', 'contract': contract.name, 'sourceMapping' : source})

        return ret
