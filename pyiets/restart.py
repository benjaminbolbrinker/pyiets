import os


def choose_mode_folders(restartfile, path, restart):
    """Chooses folders which have not been calculated yet.

    Restartability is accomplished by reading from file which
    contains folders which have been calculated previously.

    Parameters
    ----------
    restartfile : :obj:`str`
        Path to restartfile.
    path : :obj:`str`
        Path to folder containing mode_folders.

    Returns
    -------
    tuple
        mode_folders: :obj:`set` of :obj:`str`
            Absolute paths to folders which have to be calculated.
        already_done :obj:`set` of :obj:`str`
            Absolute paths to folders which have to be calculated.

    """
    cwd = os.getcwd()
    os.chdir(path)

    if os.path.exists(restartfile) and restart:
        with open(
             restartfile, 'r'
        ) as restartfile:
            already_done = set(restartfile.read().split())
            mode_folders = set([os.path.realpath(f.path) for f in
                                os.scandir(path)
                                if f.is_dir()]) - already_done
    else:
            already_done = set([])
            mode_folders = set([os.path.realpath(f.path) for f in
                                os.scandir(path)
                                if f.is_dir()])

    os.chdir(cwd)
    return (mode_folders, already_done)
