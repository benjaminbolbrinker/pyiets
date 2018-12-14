from __future__ import print_function
import sys
import json


supported_qc_progs = [
    'turbomole'
]


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def _wrongInputErrorMessage(parameter):
    eprint('Wrong input {}'.format(parameter))


def checkInput(indata):
    if indata['sp_control']['qc_prog'] not in supported_qc_progs:
        _wrongInputErrorMessage(indata['sp_control']['qc_prog'])


class InputParser():
    def __init__(self, inputfilename):
        with open(inputfilename, 'r') as infile:
            self.indata = json.load(infile)

    def getSinglePointOptions(self):
        return self.indata['sp_control']
    #  try:
    #      self.qc_progs[self.indata['sp_control']['qc_prog']]
    #  except KeyError:
    #      _wrongInputErrorMessage(self.indata['sp_control']['qc_prog'])
