import io
import os
import glob
import ase.io
from ase.calculators.turbomole import Turbomole
from contextlib import redirect_stdout


def run(params):
    """Run turbomole calculation in specified folder after cleaning directory.
    If successfull safly write foldername in file.

    Args:
        coord (str): name of turbomole coord file in folder.
        restartfilename (str): name of restartfile.
        lock (multiprocessing.Manager.lock): lock for multiprocessing.
        params (dict): ASE params for turbomole.
    """
    folder = params[0]
    options = params[1]
    restartfileloc = params[2]
    lock = params[3]
    coord = options['dissotionoutname']
    tmparams = options['sp_control']['params']

    cwd = os.getcwd()
    os.chdir(folder)

    calc = Turbomole(**tmparams)

    # Clean directory
    files = glob.glob('*')
    cleanupFiles = files
    cleanupFiles.remove(coord)
    for cleanupFile in cleanupFiles:
        os.remove(cleanupFile)

    molecule = ase.io.read(coord, format='turbomole')

    # Run
    molecule.set_calculator(calc)

    # Redirect output
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

    if restartfileloc is not None:
        restartfile = os.path.join(restartfileloc,
                                   options['sp_restart_file'])
        lock.acquire()
        with open(restartfile, 'a') as restart_file:
            restart_file.write(folder + ' ')
        lock.release()
    # else:
        # restartfile = options['sp_restart_file']

    # Safefly write to restartfile
    return folder
