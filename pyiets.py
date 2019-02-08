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
import pyiets.restart as restart
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


if __name__ == '__main__':
    WORKDIR = sys.argv[1]
    options = get_options(WORKDIR)
    options['workdir'] = os.path.realpath(WORKDIR)

    print('Parsing Input and building structures...')
    preprocess = pyiets.preprocess.Preprocessor(WORKDIR, options)

    modes = preprocess.preprocess()
    print('Done\n')

    print('Running single point calculations...')
    singlepoint = pyiets.sp.SinglePoint(WORKDIR, options)
    mode_folders = restart.choose_mode_folders(options['sp_restart_file'],
                                               options)
    singlepoint.run(mode_folders)
    print('Done\n')

    print('Running transport calculations...')
    artaios = pyiets.artaios.Artaios(WORKDIR, options)
    mode_folders = restart.choose_mode_folders(options['artaios_restart_file'],
                                               options)
    # Copy artaios input to each folder
    for folder in mode_folders:
        copyfile(os.path.join(options['workdir'],
                              options['artaios_in']),
                 os.path.join(folder, options['artaios_in']))
    artaios.run(mode_folders)
    greenmatrices_unsrt = [artaios.read_greenmatrices()[idx]
                           for idx in range(len(artaios.read_greenmatrices()))]
    print('Done\n')

    assert ((len(greenmatrices_unsrt)-1)/2 ==
            (len(artaios.mode_folders)-1)/2 ==
            (len(singlepoint.mode_folders)-1)/2 == len(modes))

    print('Calculating Troisi-Greensmatrices...')
    troisi = Troisi(options=options, modes=modes,
                    greenmat_dictarr=greenmatrices_unsrt)
    troisi.calc_greensmatrices()
    print('Done\n')

    print('Calculating iets spectrum...')
    troisi.calc_IET_spectrum()
    print('Done\n')

    print('Printing to file...')
    troisi.write_IET_spectrum(os.path.join(WORKDIR,
                              options['iets_output_file']))
    print('Done\n')

    print('pyIETS terminated normally')
