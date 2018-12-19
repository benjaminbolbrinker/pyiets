import multiprocessing

import pyiets.runcalcs.turbomole as turbomole


def start_tm_single_points(folders, coord, params,
                           nthreads, restartfilename):
    with multiprocessing.Pool(processes=nthreads) as pool:
        manager = multiprocessing.Manager()
        lock = manager.Lock()
        params = [(coord, restartfilename, lock, folder, params)
                  for folder in folders]
        pool.starmap(turbomole.run, params)
