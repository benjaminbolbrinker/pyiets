from __future__ import print_function
import sys
import json


supported_qc_progs = [
    'turbomole'
]


def _wrongInputErrorMessage(parameter):
    print('Wrong input {}'.format(parameter), file=sys.stderr)


class InputParser():
    def __init__(self, inputfilename):
        with open(inputfilename, 'r') as infile:
            self.indata = json.load(infile)

    def getSinglePointOptions(self):
        try:
            supported_qc_progs.index(self.indata['sp_control']['qc_prog'])
        except ValueError:
            _wrongInputErrorMessage(self.indata['sp_control']['qc_prog'])
            raise SystemExit
        return self.indata
    #  try:
    #      self.qc_progs[self.indata['sp_control']['qc_prog']]
    #  except KeyError:
    #      _wrongInputErrorMessage(self.indata['sp_control']['qc_prog'])
