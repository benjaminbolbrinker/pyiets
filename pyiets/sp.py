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
#  import pyiets.io.snfio
#  import pyiets.io.createInput
import pyiets.runcalcs.calcmanager as calcmanager
#  import pyiets.io.checkinput
#  import pyiets.read


class SinglePoint():
    def __init__(self, mode_folders, options, restartsaveloc=None):
        self.options = options
        self.mode_folders = mode_folders
        self.restartsaveloc = restartsaveloc

    def run(self):
        """Read snf output file and run turbomole calculations
        for every vibration mode. Calculation is controlled via 'input.json'

        Args:
            path (str): path to inputfiles ('snf.out' and 'input.json')
        """
        cwd = os.getcwd()
        os.chdir(self.options['workdir'])
        if self.options['sp_control']['qc_prog'] == 'turbomole':
            calcmanager.start_tm_single_points(self.mode_folders, self.options,
                                               self.restartsaveloc)
        os.chdir(cwd)
