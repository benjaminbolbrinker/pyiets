#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import pyiets.sp
import pyiets.artaios


def get_options(path):
    options = pyiets.read.infile('input_defaults.json')
    cwd = os.getcwd()
    os.chdir(path)
    options.update(pyiets.read.infile(options['input_file']))
    pyiets.io.checkinput.check_options(options)
    os.chdir(cwd)
    return options


if __name__ == '__main__':
    workdir = sys.argv[1]
    opt = get_options(workdir)
    pyiets.sp.run(workdir, opt)
    pyiets.artaios.run(workdir, opt)
