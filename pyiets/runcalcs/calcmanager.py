import os
import multiprocessing

import pyiets.runcalcs.turbomole as turbomole


def start_tm_single_points_sp(outfolder, calc_options):
    mode_folders = [f.path for f in os.scandir(outfolder) if f.is_dir()]
    for mode_folder in mode_folders:
        if turbomole.run(mode_folder, calc_options):
            with open('restart.dat', 'a') as restart_file:
                restart_file.write(mode_folder + ' ')


def start_tm_single_points_mp(outfolder, calc_options, nthreads):
    mode_folders = [f.path for f in os.scandir(outfolder) if f.is_dir()]

    processes = [multiprocessing.Process(target=turbomole.run,
                                         args=(folder, calc_options))
                 for folder in mode_folders]
    for i in range(0, len(processes), nthreads):
        [process.start() for process in processes[i:i+nthreads]]
        [process.join() for process in processes[i:i+nthreads]]


def restart_tm_single_points_sp(outfolder, calc_options):
    mode_folders = [f.path for f in os.scandir(outfolder) if f.is_dir()]
    for mode_folder in mode_folders:
        turbomole.run(mode_folder, calc_options)


def restart_tm_single_points_mp(outfolder, calc_options, nthreads):
    mode_folders = [f.path for f in os.scandir(outfolder) if f.is_dir()]

    processes = [multiprocessing.Process(target=turbomole.run,
                                         args=(folder, calc_options))
                 for folder in mode_folders]
    for i in range(0, len(processes), nthreads):
        [process.start() for process in processes[i:i+nthreads]]
        [process.join() for process in processes[i:i+nthreads]]
