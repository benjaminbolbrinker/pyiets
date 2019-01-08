import io
import os
import glob
import ase.io
from ase.calculators.turbomole import Turbomole
from contextlib import redirect_stdout

import subprocess


def run(folder, mosfile, options, lock):
    """Run turbomole calculation in specified folder after cleaning directory.
    If successfull safly write foldername in file.

    Args:
        coord (str): name of turbomole coord file in folder.
        restartfilename (str): name of restartfile.
        lock (multiprocessing.Manager.lock): lock for multiprocessing.
        params (dict): ASE params for turbomole.
    """

    cwd = os.getcwd()
    subprocess.call(['cp', os.path.realpath(options['artaios_in']), folder])
    os.chdir(folder)

    # Run and redirect output
    tmoutname = 'artaios.out'
    print('''
Starting artaios in \'{}\'
Redirecting output to \'{}\'
'''.format(folder, tmoutname))
    f = io.StringIO()
    with open(tmoutname, 'w') as f:
        with redirect_stdout(f):
            pass
            #  subprocess.Popen(os.path.join(options['artaios'],
            #                                options['artaios_bin']) + ' ',
            #                   options['artaios_in'] + ' ',
            #                   '> ',
            #                   options['artaios_out'])

    os.chdir(cwd)

    # Safefly write to restartfile
    lock.acquire()
    with open(options['artaios_restart_file'], 'a') as restart_file:
        restart_file.write(folder + ' ')
    lock.release()
    return folder
