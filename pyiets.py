#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pyIETS — A code for calculating inelastic tunneling spectra

This program calculates inelastic tunneling spectra of
molecules between molecular junctions using the ansatz from Troisi[1].
It reads vibrational modes from the output of the program SNF [2] which
is part of the MoViPac package [3]. For each mode two static single-
point calculations are performed - one for each distorted molecule -
using Turbomole[4]. Greensmatrices are calculated using the code ARTAIOS[5]
for each distorted molecule.

Example
-------
Examples are provided in `tests/`. Type

    $ make test_all

to test the correct installation of this module.

References
-----
    This is an example of an indented section. It's like any other section,
    but the body is indented to help it stand out from surrounding text.=
    [1] Troisi, A. (2008). Inelastic electron tunnelling in saturated molecules
    with different functional groups: correlations and symmetry considerations
    from a computational study. Journal of Physics: Condensed Matter,
    20(37), 374111.
    [2] J. Neugebauer, M. Reiher, C. Kind, B. A. Hess, J. Comput. Chem. 23
    2002, 895-910.
    [3] T. Weymuth, M. P. Haag, K. Kiewisch, S. Luber, S. Schenk, Ch. R. Jacob,
    C. Herrmann, J. Neugebauer, M. Reiher, MOVIPAC: Vibrational spectroscopy
    with a robust meta-program for massively parallel standard and inverse
    calculations, J. Chem. Comput., 2012, DOI: 10.1002/jcc.23036.
    [4] TURBOMOLE V6.2 2010, a development of University of Karlsruhe and
    Forschungszentrum Karlsruhe GmbH, 1989-2007, TURBOMOLE GmbH, since 2007;
    available from http://www.turbomole.com.w
    [5] M. Deffner, L. Groß, T. Steenbock, B. A. Voigt, G. C. Solomon,
    and C. Herrmann. Artaios — a  code for postprocessing quantum chemical
    electronic structure calculations, available from
    https://www.chemie.uni-hamburg.de/ac/herrmann/software/index.html
    (2008-2017)


Please cite this work as
    [n] B. Bolbrinker, M. Deffner, M. Zoellner, and C. Herrmann.
    pyIETS — a code for calculating inelastic tunneling spectra, available from
    https://github.com/
"""

# PyIETS

# Postprocessing tool for calculating inelastic tunneling spectra
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
    mode_folders, done = restart.choose_mode_folders(
            os.path.join(options['workdir'],
                         options['mode_folder'],
                         options['sp_restart_file']),
            options)
    # print(os.path.join(options['sp_restart_file'],
                       # options['mode_folder'],
                       # options['sp_restart_file']))
    # print(mode_folders)
    # print(done)
    singlepoint = pyiets.sp.SinglePoint(
        mode_folders, options,
        restartsaveloc=os.path.join(options['workdir'],
                                    options['mode_folder']))
    singlepoint.run()
    print('Done\n')

    print('Running transport calculations...')
    mode_folders, done = restart.choose_mode_folders(
            os.path.join(options['workdir'],
                         options['mode_folder'],
                         options['artaios_restart_file']),
            options)
    artaios = pyiets.artaios.Artaios(
            mode_folders, options,
            restartsaveloc=os.path.join(options['workdir'],
                                        options['mode_folder']))

    # Copy artaios input to each folder
    for folder in mode_folders:
        copyfile(os.path.join(options['workdir'],
                              options['artaios_in']),
                 os.path.join(folder, options['artaios_in']))
    artaios.run()
    g_files = [os.path.join(m, options['greenmatrix_file'])
               for m in mode_folders.union(done)]
    greenmatrices_unsrt = [artaios.read_greenmatrices(g_files)[idx]
                           for idx in range(len(artaios.read_greenmatrices(
                               g_files)))]
    print('Done\n')

    print('Calculating Troisi-Greensmatrices...')
    troisi = Troisi(options=options, modes=modes,
                    greenmat_dictarr=greenmatrices_unsrt)
    troisi.calc_greensmatrices()
    print('Done\n')

    print('Calculating iets spectrum...')
    troisi.calc_IET_spectrum()
    print('Done\n')

    print('Printing to file...')
    troisi.write_IET_spectrum(os.path.join(options['workdir'],
                              options['iets_output_file']))
    print('Done\n')

    print('pyIETS terminated normally')
