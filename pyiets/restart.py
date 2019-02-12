import os


def choose_mode_folders(restartfile, path):
    """Example function with types documented in the docs

    `PEP 484`_ type annotations are supported. If attribute, parameter, and
    return types are annotated according to `PEP 484`_, they do not need to be
    included in the docstring:

    Parameters
    ----------
    param1 : int
        The first parameter.
    param2 : str
        The second parameter.

    Returns
    -------
    bool
        True if successful, False otherwise.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/

    """
    cwd = os.getcwd()
    os.chdir(path)

    if os.path.exists(restartfile):
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
