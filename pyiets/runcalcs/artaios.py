import os
import subprocess


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

    cwd = os.getcwd()
    os.chdir(folder)
    # Run and redirect output
    stdoutname = options['artaios_stdout']
    stderrname = options['artaios_stderr']
    print('''
Starting artaios in \'{}\'
Redirecting output to \'{}\' and \'{}\'
'''.format(folder, stdoutname, stderrname))

    # Run and redirect output
    process = subprocess.Popen(os.path.join(options['artaios'],
                               options['artaios_bin']) + ' '
                               + options['artaios_in'],
                               shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    with open(stdoutname, 'wb') as f:
        for line in process.stdout:
            f.write(line)

    with open(stderrname, 'wb') as f:
        for line in process.stderr:
            f.write(line)

    os.chdir(cwd)

    # Safely write to restartfile
    lock.acquire()
    if restartfileloc is not None:
        restartfile = os.path.join(restartfileloc,
                                   options['artaios_restart_file'])
    else:
        restartfile = options['artaios_restart_file']

    with open(restartfile, 'a') as restart_file:
        restart_file.write(folder + ' ')
    lock.release()
    return folder
