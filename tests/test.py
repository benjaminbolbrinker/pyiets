#!/usr/bin/env python3

import sys
import os
import math

import numpy as np


test_dirs = ['H2O_dscf',
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
    iets_test = np.loadtxt(os.path.join(test, 'test.dat'), dtype={
        'names': ('mode_idx', 'wavenumber', 'energy', 'intensity'),
        'formats': ('i8', 'f8', 'f8', 'f8')
    })

    iets = np.loadtxt(os.path.join(test, 'iets.dat'), dtype={
        'names': ('mode_idx', 'wavenumber', 'energy', 'intensity'),
        'formats': ('i8', 'f8', 'f8', 'f8')
    })
    for idx, inten in enumerate(iets['intensity']):
        if not math.isclose(inten, iets_test['intensity'][idx], rel_tol=1e-04):
            print(test + ' - NOT OK. Terminating in line ', idx, '...')
            print(inten, iets_test['intensity'][idx])
            sys.exit()
    print(test + ' - OK')
