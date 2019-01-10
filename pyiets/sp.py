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
import pyiets.io.snfio
import pyiets.io.createInput
import pyiets.runcalcs.calcmanager as calcmanager
import pyiets.io.checkinput
import pyiets.read


def run(path, options):
    """Read snf output file and run turbomole calculations
    for every vibration mode. Calculation is controlled via 'input.json'

    Args:
        path (str): path to inputfiles ('snf.out' and 'input.json')
    """
    cwd = os.getcwd()
    os.chdir(path)

    snfparser = pyiets.io.snfio.SnfParser(snfoutname=options['snf_out'])
    dissotionoutname = snfparser.get_molecule().to_ASE_atoms_obj() \
        .get_chemical_formula(mode='hill') + '.' + str(
            options['sp_control']['qc_prog'])

    if not os.path.exists(options['mode_folder']):
        pyiets.io.createInput.writeDisortion(dissotionoutname,
                                             options['mode_folder'],
                                             options['sp_control']['qc_prog'],
                                             options['snf_out'],
                                             delta=options['delta'])

    if os.path.exists(options['sp_restart_file']):
        with open(options['sp_restart_file'], 'r') as restartfile:
            mode_folders = set([f.path for f in
                                os.scandir(options['mode_folder'])
                                if f.is_dir()]) \
                            - set(restartfile.read().split())
    else:
            mode_folders = set([f.path for f in
                                os.scandir(options['mode_folder'])
                                if f.is_dir()])

    if options['sp_control']['qc_prog'] == 'turbomole':
        calcmanager.start_tm_single_points(mode_folders,
                                           dissotionoutname,
                                           options['sp_control']['params'],
                                           options['mp'],
                                           options['sp_restart_file'])
    os.chdir(cwd)