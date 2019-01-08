import os
import pyiets.runcalcs.calcmanager as calcmanager


def run(path, options):
    """Read tm mos files and run artaios calculations
    for every vibration mode. Calculation is controlled via 'input.json'

    Args:
        path (str): path to inputfiles ('artaios.in' and 'input.json')
                    and mode_folder containing previously
                    calculated single points corresponding to different
                    normal-modes.
    """
    cwd = os.getcwd()
    os.chdir(path)
    mos_name = 'mos'

    if os.path.exists(options['artaios_restart_file']):
        with open(options['artaios_restart_file'], 'r') as restartfile:
            mode_folders = set([f.path for f in
                                os.scandir(options['mode_folder'])
                                if f.is_dir()]) \
                            - set(restartfile.read().split())
    else:
            mode_folders = set([f.path for f in
                                os.scandir(options['mode_folder'])
                                if f.is_dir()])

    if options['sp_control']['qc_prog'] == 'turbomole':
        calcmanager.get_greens(mode_folders,
                               mos_name,
                               options)
    os.chdir(cwd)
