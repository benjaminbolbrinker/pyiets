import os


def choose_mode_folders(restartfile, options):
    cwd = os.getcwd()
    os.chdir(options['workdir'])

    if os.path.exists(restartfile):
        with open(
             restartfile, 'r'
        ) as restartfile:
            already_done = set(restartfile.read().split())
            mode_folders = set([os.path.realpath(f.path) for f in
                                os.scandir(options['mode_folder'])
                                if f.is_dir()]) - already_done
    else:
            already_done = set([])
            mode_folders = set([os.path.realpath(f.path) for f in
                                os.scandir(options['mode_folder'])
                                if f.is_dir()])

    os.chdir(cwd)
    return (mode_folders, already_done)
