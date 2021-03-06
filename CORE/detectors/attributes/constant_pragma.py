"""
    Check that the same pragma is used in all the files
"""

from securewei.detectors.abstract_detector import AbstractDetector, DetectorClassification


class ConstantPragma(AbstractDetector):
    """
    Check that the same pragma is used in all the files
    """

    ARGUMENT = 'pragma'
    HELP = 'if different pragma directives are used'
    IMPACT = DetectorClassification.INFORMATIONAL
    CONFIDENCE = DetectorClassification.HIGH

    def detect(self):
        results = []
        pragma = self.securewei.pragma_directives
        versions = [p.version for p in pragma]
        versions = list(set(versions))

        if len(versions) > 1:
            info = "Different version of Solidity used in {}: {}".format(self.filename, versions)
            self.log(info)

            source = [p.source_mapping for p in pragma]

            results.append({'vuln': 'ConstantPragma',
                            'versions': versions,
                            'sourceMapping': source})

        return results
