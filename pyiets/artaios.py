# PyIETS

# Postprocessing tool for calculating the IETS intensity and hence the
# electron-phonon-interaction
#
# Copyright (C) 2019 Benjamin Bolbrinker, Michael Deffner, Carmen Herrmann
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
import pyiets.runcalcs.calcmanager as calcmanager


def run(path, options):
    """Read tm mos files and run artaios calculations
    for every vibration mode. Calculation is controlled via 'input.json'

    Args:
        path (str): path to inputfiles ('artaios.in' and 'input.json')
                    and mode_folder containing previously
                    calculated single points corresponding to different
                    normal-modes.
    """
    cwd = os.getcwd()
    os.chdir(path)
    mos_name = 'mos'

    if os.path.exists(options['artaios_restart_file']):
        with open(options['artaios_restart_file'], 'r') as restartfile:
            mode_folders = set([f.path for f in
                                os.scandir(options['mode_folder'])
                                if f.is_dir()]) \
                            - set(restartfile.read().split())
    else:
            mode_folders = set([f.path for f in
                                os.scandir(options['mode_folder'])
                                if f.is_dir()])

    if options['sp_control']['qc_prog'] == 'turbomole':
        calcmanager.get_greens(mode_folders,
                               mos_name,
                               options)
    os.chdir(cwd)
