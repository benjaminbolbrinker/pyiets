import io
import os
import sys
import glob
import ase.io
from ase.calculators.turbomole import Turbomole
from contextlib import redirect_stdout


def run(restartfilename, lock, folder, paramdict):
    """TODO: to be defined1. """
    cwd = os.getcwd()
    os.chdir(folder)

    calc = Turbomole(**paramdict['params'])

    files = glob.glob('*')
    if len(files) == 1:
        coord = files[0]
    elif len(files) == 0:
        print('Something went terribly wrong!', file=sys.stderr)
        raise SystemExit
    else:
        cleanupFiles = files
        cleanupFiles.remove('H2O.turbomole')
        for cleanupFile in cleanupFiles:
            os.remove(cleanupFile)
        coord = 'H2O.turbomole'

    molecule = ase.io.read(coord, format='turbomole')
    molecule.set_calculator(calc)

    tmoutname = 'turbomole.out'
    print('''
Starting turbomole in \'{}\'
Redirecting output to \'{}\'
'''.format(folder, tmoutname))
    f = io.StringIO()
    with open(tmoutname, 'w') as f:
        with redirect_stdout(f):
            molecule.get_potential_energy()
    os.chdir(cwd)
    lock.acquire()
    with open(restartfilename, 'a') as restart_file:
        restart_file.write(folder + ' ')
    lock.release()
    return folder
