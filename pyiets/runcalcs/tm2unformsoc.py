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
    os.remove(options['greenmatrix_file'])
    # os.path.join(options['greenmatrix_file'], '.old'))
    stdoutname = 'artaios_tm_soc.stdout'
    stderrname = 'artaios_tm_soc.stderr'
    if options['verbose']:
        print('''
Starting tm2unformsoc in \'{}\'
Redirecting output to \'{}\' and \'{}\'
'''.format(folder, stdoutname, stderrname))

    # Run and redirect output
    process = subprocess.Popen(options['artaios_tm_soc_bin'],
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
