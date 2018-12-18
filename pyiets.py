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
    inparser = pyiets.io.parseInput.InputParser('input.json')
    options = inparser.getSinglePointOptions()
    qc_prog = options['sp_control']['qc_prog']
    pyiets.io.createInput.writeDisortion(qc_prog, 'snf.out', delta=0.1)
    calcmanager.start_tm_single_points_mp(options, 6)
