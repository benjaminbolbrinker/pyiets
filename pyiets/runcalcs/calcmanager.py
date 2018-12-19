import multiprocessing

import pyiets.runcalcs.turbomole as turbomole


def start_tm_single_points(folders, calc_options,
                           nthreads, restartfilename):
    with multiprocessing.Pool(processes=nthreads) as pool:
        manager = multiprocessing.Manager()
        lock = manager.Lock()
        params = [(restartfilename, lock, folder, calc_options)
                  for folder in folders]
        pool.starmap(turbomole.run, params)
