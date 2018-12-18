#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from glob import glob
import pyiets.io.snfio
import pyiets.io.createInput
import pyiets.io.parseInput
import pyiets.runcalcs.calcmanager as calcmanager

if __name__ == '__main__':
    os.chdir(sys.argv[1])
    inparser = pyiets.io.parseInput.InputParser('input.json')
    options = inparser.getSinglePointOptions()
    qc_prog = options['sp_control']['qc_prog']
    outfolder = pyiets.io.createInput.create_ascending_name('dissortions')
    print(glob('./*/'))
    if 'folder' in options:
        outfolder = pyiets.io.createInput\
                    .create_ascending_name(options['folder'])

    pyiets.io.createInput.writeDisortion(outfolder, qc_prog,
                                         'snf.out', delta=0.1)
    calcmanager.start_tm_single_points_mp(outfolder, options, 6)
