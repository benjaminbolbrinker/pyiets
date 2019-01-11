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

    cwd = os.getcwd()
    subprocess.call(['cp', os.path.realpath(options['artaios_in']), folder])
    os.chdir(folder)

    stdoutname = 'artaios_tm.stdout'
    stderrname = 'artaios_tm.stderr'
    print('''
Starting tm2unformcl in \'{}\'
Redirecting output to \'{}\' and \'{}\'
'''.format(folder, stdoutname, stderrname))

    # Run and redirect output
    process = subprocess.Popen(os.path.join(options['artaios'],
                                            options['artaios_tm_bin']),
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
