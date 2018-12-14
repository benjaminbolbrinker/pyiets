import os

import pyiets.io.createInput
import pyiets.io.parseInput
import pyiets.runcalcs.turbomole as turbomole


def startSinglePoints(calc_options):
    outdir = pyiets.io.createInput.outdir
    mode_folders = [f.path for f in os.scandir(outdir) if f.is_dir()]
    for mode_folder in mode_folders:
        turbomole.run(calc_options)


def startSinglePoints_threaded(calc_options):
    outdir = pyiets.io.createInput.outdir
    mode_folders = [f.path for f in os.scandir(outdir) if f.is_dir()]
    for mode_folder in mode_folders:
        turbomole.run(calc_options)
