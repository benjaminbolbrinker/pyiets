import io
import os
import glob
import ase.io
from ase.calculators.gaussian import Gaussian
from contextlib import redirect_stdout


def run(params):
    """Run Turbomole calculation in specified folder.
    Removes all files before starting calculation.
    If successful safly write foldername in file. (Therefore
    lock has to be provided)

    Parameters
    ----------
        params : :obj:`list`
            folder : obj`str`
                name of folder to perform calculation in.
            options : :obj`dict`
                Options.
            restartfilename : :obj:`str`
                path to restartfile.
            lock : :obj:`multiprocessing.Manager.lock`
                lock for multiprocessing.
    """
    folder = params[0]
    options = params[1]
    restartfileloc = params[2]
    lock = params[3]

    coord = options['dissotionoutname']
    g09params = options['sp_control']['params']

    cwd = os.getcwd()
    os.chdir(folder)

    calc = Gaussian(**g09params)

    # Clean directory
    files = glob.glob('*')
    cleanupFiles = files
    cleanupFiles.remove(coord)
    for cleanupFile in cleanupFiles:
        os.remove(cleanupFile)

    molecule = ase.io.read(coord, format='xyz')

    # Run
    molecule.set_calculator(calc)

    # Redirect output
    tmoutname = 'gaussian.stdout'
    if options['verbose']:
        print('''
Starting gaussian in \'{}\'
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
