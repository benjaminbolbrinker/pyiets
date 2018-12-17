import os
import multiprocessing

import pyiets.io.createInput
import pyiets.io.parseInput
import pyiets.runcalcs.turbomole as turbomole


def startSinglePoints_sp(calc_options):
    outdir = pyiets.io.createInput.outdir
    mode_folders = [f.path for f in os.scandir(outdir) if f.is_dir()]
    for mode_folder in mode_folders:
        turbomole.run(mode_folder, calc_options)


def startSinglePoints_mp(calc_options, nthreads):
    outdir = pyiets.io.createInput.outdir
    mode_folders = [f.path for f in os.scandir(outdir) if f.is_dir()]

    processes = [multiprocessing.Process(target=turbomole.run,
                                         args=(folder, calc_options))
                 for folder in mode_folders]
    for i in range(0, len(processes), nthreads):
        [process.start() for process in processes[i:i+nthreads]]
        [process.join() for process in processes[i:i+nthreads]]
