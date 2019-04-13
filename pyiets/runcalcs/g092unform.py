import os
import subprocess


def run(params):
    """Run artaios preprocess script in specified folder.

    Parameters
    ----------
        params : :obj:`list`
            folder : obj`str`
                name of folder to perform calculation in.
            options : :obj`dict`
                Options.
    """

    folder = params[0]
    options = params[1]

    cwd = os.getcwd()
    # subprocess.call(['cp', os.path.realpath(options['artaios_in']), folder])
    os.chdir(folder)

    stdoutname = 'artaios_g09.stdout'
    stderrname = 'artaios_g09.stderr'
    if options['verbose']:
        print('''
Starting g09_2unform in \'{}\'
Redirecting output to \'{}\' and \'{}\'
'''.format(folder, stdoutname, stderrname))

    # Run and redirect output
    process = subprocess.Popen(options['artaios_gm_bin'] + " "
                               + "g09.log" + " "
                               + str(options['artaios_gm_bin_spin_comp']),
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
