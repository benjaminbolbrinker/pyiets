import os
import sys
import glob
import ase.io
from ase.calculators.turbomole import Turbomole


def run(folder, paramdict):
    #  cwd = os.getcwd()
    #  print(cwd)
    #  os.chdir(folder)
    print('Using turbomole...')
    calc = Turbomole(define_str=paramdict['sp_control']['define_string'])

    files = glob.glob(folder + '/*')
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
