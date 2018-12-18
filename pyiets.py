#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import pyiets.io.snfio
import pyiets.io.createInput
import pyiets.io.parseInput
import pyiets.runcalcs.calcmanager as calcmanager

if __name__ == '__main__':
    os.chdir(sys.argv[1])
    infile = 'input.json'
    inparser = pyiets.io.parseInput.InputParser(infile)
    options = inparser.getSinglePointOptions()
    qc_prog = options['sp_control']['qc_prog']
    restart = False
    restartfile = pyiets.io.createInput.create_ascending_name('pyiets.restart')
    mp = 1

    if 'mp' in options:
        mp = options['mp']

    if 'restart' in options:
        restart = options['restart']

    if restart:
        folder = pyiets.io.createInput.find_descending_dirname('./')
        if 'folder' in options:
            folder = options['folder']
        if mp == 1:
            calcmanager.restart_tm_single_points_sp(folder, options,
                                                    restartfile)
        elif mp > 1:
            calcmanager.restart_tm_single_points_mp(folder, options, mp,
                                                    restartfile)
        else:
            pyiets.io.parseInput._wrongInputErrorMessage(mp, infile)
    else:
        outfolder = pyiets.io.createInput.create_ascending_name('dissortions')
        if 'folder' in options:
            outfolder = pyiets.io.createInput \
                        .create_ascending_name(options['folder'])
        pyiets.io.createInput.writeDisortion(outfolder, qc_prog,
                                             'snf.out', delta=0.1)
        if mp == 1:
            calcmanager.start_tm_single_points_sp(outfolder, options,
                                                  restartfile)
        elif mp > 1:
            calcmanager.start_tm_single_points_mp(outfolder, options, mp,
                                                  restartfile)
        else:
            pyiets.io.parseInput._wrongInputErrorMessage(mp, infile)
