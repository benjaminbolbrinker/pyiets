import io
import os
import sys
import glob
import ase.io
from ase.calculators.turbomole import Turbomole
from contextlib import redirect_stdout


def run_sp(restartfilename, folder, paramdict):
    cwd = os.getcwd()
    os.chdir(folder)

    if 'params' in paramdict['sp_control']:
        calc = Turbomole(**paramdict['sp_control']['params'])
    else:
        print('''Missing turbomole configuration!
Add \'define_string\' or \'params\' in \'sp_control\'
              ''', file=sys.stderr)
        raise SystemExit

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

        #  calc.set(restart=True)

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
    with open(restartfilename, 'a') as restart_file:
        restart_file.write(folder + ' ')
    return folder


def run_mp(restartfilename, lock, folder, paramdict):
    cwd = os.getcwd()
    os.chdir(folder)

    if 'params' in paramdict['sp_control']:
        calc = Turbomole(**paramdict['sp_control']['params'])
    else:
        print('''Missing turbomole configuration!
Add \'define_string\' or \'params\' in \'sp_control\'
              ''', file=sys.stderr)
        raise SystemExit

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
        #  calc.set(restart=True)

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
