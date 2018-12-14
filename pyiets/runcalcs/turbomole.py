import os
import sys
import glob
import ase.io
from ase.calculators.turbomole import Turbomole


def run(folder, paramdict):
    print('Using turbomole...')
    cwd = os.getcwd()
    os.chdir(folder)

    calc = Turbomole(define_str=paramdict['sp_control']['define_string'])

    files = glob.glob('*')
    if len(files) == 1:
        coord = files[0]
    elif len(files) == 0:
        print('Something went terribly wrong!', file=sys.stderr)
        raise SystemExit
    else:
        calc.set(restart=True)

    molecule = ase.io.read(coord, format='turbomole')
    molecule.set_calculator(calc)

    molecule.get_potential_energy()

    os.chdir(cwd)
