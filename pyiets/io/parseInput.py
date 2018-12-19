from __future__ import print_function
import sys
import json


supported_qc_progs = [
    'turbomole'
]


def _wrongInputErrorMessage(parameter, filename):
    print('Wrong input \'{}\' in {}'.format(parameter, filename),
          file=sys.stderr)


class InputParser():
    def __init__(self, inputfilename):
        self.inputfilename = inputfilename
        with open(inputfilename, 'r') as infile:
            self.indata = json.load(infile)

    def getSinglePointOptions(self):
        return self.indata
