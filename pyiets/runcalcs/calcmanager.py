import os
import multiprocessing

import pyiets.runcalcs.turbomole as turbomole


def start_tm_single_points_sp(outfolder, calc_options, restartfilename):
    mode_folders = {f.path for f in os.scandir(outfolder) if f.is_dir()}
    for mode_folder in mode_folders:
        turbomole.run_sp(restartfilename, mode_folder, calc_options)


def start_tm_single_points_mp(outfolder, calc_options,
                              nthreads, restartfilename):
    mode_folders = {f.path for f in os.scandir(outfolder) if f.is_dir()}
    pool = multiprocessing.Pool(processes=nthreads)
    manager = multiprocessing.Manager()
    lock = manager.Lock()
    params = [(restartfilename, lock, mode_folder, calc_options)
              for mode_folder in mode_folders]

    pool.starmap(turbomole.run_mp, params, chunksize=1)


def restart_tm_single_points_sp(outfolder, calc_options, restartfilename):
    with open(restartfilename, 'r') as restartfile:
        mode_folders = set([f.path for f in os.scandir(outfolder)
                            if f.is_dir()]) - set(restartfile.read().split())

    for mode_folder in mode_folders:
        turbomole.run_sp(restartfilename, mode_folder, calc_options)


def restart_tm_single_points_mp(outfolder, calc_options,
                                nthreads, restartfilename):
    with open(restartfilename, 'r') as restartfile:
        mode_folders = set([f.path for f in os.scandir(outfolder)
                            if f.is_dir()]) - set(restartfile.read().split())

    pool = multiprocessing.Pool(processes=nthreads)
    manager = multiprocessing.Manager()
    lock = manager.Lock()
    params = [(restartfilename, lock, mode_folder, calc_options)
              for mode_folder in mode_folders]

    pool.starmap(turbomole.run_mp, params, chunksize=1)
