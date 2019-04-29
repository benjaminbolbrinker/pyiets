#!/usr/bin/env python3

import sys
import os
import filecmp


test_dirs = ['C10H4Au6S2_dscf',
             'C10H4Au6S2_ridft',
             'H2O_dscf',
             'H2O_dscf_gaussian',
             'H2O_dscf_tm_parms',
             'H2O_M',
             'H2O_ridft',
             'H2O_ridft_fakegaussianin',
             'H2O_ridft_gaussianin',
             'H2O_ridft_tm_params',
             'H2O_ridft_turbomolein_M',
             'H2O_self']

test_dirs = [os.path.join(os.path.dirname(__file__), test)
             for test in test_dirs]

for test in test_dirs:
    if filecmp.cmp(os.path.join(test, 'iets.dat'),
                   os.path.join(test, 'test.dat')):
        print(test + ' - OK')
    else:
        print(test + ' - NOT OK. Terminating...')
        sys.exit()
