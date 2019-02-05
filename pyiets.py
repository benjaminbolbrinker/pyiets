#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PyIETS

# Postprocessing tool for calculating the IETS intensity and hence the
# electron-phonon-interaction
#
# Copyright (C) 2019 Benjamin Bolbrinker, Michael Deffner,
#                    Martin Zoellner, Carmen Herrmann
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os
import sys
import pyiets.sp
import pyiets.preprocess
import pyiets.artaios
import pyiets.read
import pyiets.io.checkinput
from pyiets.troisi import Troisi
from shutil import copyfile


def get_options(path):
    options = pyiets.read.infile('input_defaults.json')
    cwd = os.getcwd()
    os.chdir(path)
    options.update(pyiets.read.infile(options['input_file']))
    pyiets.io.checkinput.check_options(options)
    os.chdir(cwd)
    return options


def run_artaios(artaiosobj):
    cwd = os.getcwd()
    os.chdir(WORKDIR)

    if os.path.exists(options['artaios_restart_file']):
        with open(
             options['artaios_restart_file'], 'r'
        ) as restartfile:
            mode_folders = set([os.path.realpath(f.path) for f in
                                os.scandir(options['mode_folder'])
                                if f.is_dir()]) \
                              - set(restartfile.read().split())
    else:
            mode_folders = set([os.path.realpath(f.path) for f in
                                os.scandir(options['mode_folder'])
                                if f.is_dir()])

    # Copy artaios input to each folder
    for folder in mode_folders:
        copyfile(os.path.join(options['workdir'],
                              options['artaios_in']),
                 os.path.join(folder, options['artaios_in']))

    os.chdir(cwd)

    artaiosobj.run(mode_folders)


if __name__ == '__main__':
    WORKDIR = sys.argv[1]
    options = get_options(WORKDIR)
    options['workdir'] = os.path.realpath(WORKDIR)
    preprocess = pyiets.preprocess.Preprocessor(WORKDIR, options)
    modes = preprocess.writeDisortion(options)

    singlepoint = pyiets.sp.SinglePoint(WORKDIR, options)
    singlepoint.run()
    artaios = pyiets.artaios.Artaios(WORKDIR, options)

    run_artaios(artaios)

    greenmatrices_unsrt = [artaios.read_greenmatrices()[idx]
                           for idx in range(len(artaios.read_greenmatrices()))]

    assert ((len(greenmatrices_unsrt)-1)/2 ==
            (len(artaios.mode_folders)-1)/2 ==
            (len(singlepoint.modes_to_calc)-1)/2 == len(modes))

    troisi = Troisi(options=options, modes=modes,
                    greenmat_dictarr=greenmatrices_unsrt)

    # troisi.calc_greensmatrix(2)
    troisi.calc_greensmatrices()
    print(troisi.troisi_greenmatrices)
    troisi.calc_IET_spectrum()
