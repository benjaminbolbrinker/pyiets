import multiprocessing

import pyiets.runcalcs.turbomole as turbomole


def start_tm_single_points(folders, coord, params,
                           nthreads, restartfilename):
    '''Start turbomole calculations asynchronously in specified folders.

    Args:
        folders (list): containing foldernames (str)
        coord (str): name of turbomole coord file (has to be present in each
                     folder).
        params (dict): ASE params for turbomole.
        nthreads (int): number of threads.
        restartfilename (str): name of restartfile.
    '''
    with multiprocessing.Pool(processes=nthreads) as pool:
        manager = multiprocessing.Manager()
        lock = manager.Lock()
        params = [(coord, restartfilename, lock, folder, params)
                  for folder in folders]
        pool.starmap(turbomole.run, params)
