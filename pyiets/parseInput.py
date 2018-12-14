from __future__ import print_function
import sys
import json

import runcalcs.turbomole

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
           

def _wrongInputErrorMessage(parameter):
    eprint('Wrong input {}'.format(parameter))


class InputParser():
    def __init__(self, inputfilename): 
        with open(inputfilename, 'r') as infile:
            self.indata = json.load(infile)
        self.qc_progs = {'turbomole': runcalcs.turbomole.run(self.indata['sp_control'])}
        try:
            self.qc_progs[self.indata['sp_control']['qc_prog']]
        except KeyError:
            _wrongInputErrorMessage(self.indata['sp_control']['qc_prog'])