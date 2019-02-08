import os


def choose_mode_folders(mode, restartfile, options):
    cwd = os.getcwd()
    os.chdir(options['workdir'])

    if os.path.exists(restartfile):
        with open(
             restartfile, 'r'
        ) as restartfile:
            mode_folders = set([os.path.realpath(f.path) for f in
                                os.scandir(options['mode_folder'])
                                if f.is_dir()]) \
                              - set(restartfile.read().split())
    else:
            mode_folders = set([os.path.realpath(f.path) for f in
                                os.scandir(options['mode_folder'])
                                if f.is_dir()])

    os.chdir(cwd)
    return mode_folders
