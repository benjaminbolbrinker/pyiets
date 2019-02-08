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
    def __init__(self, options):
        self.options = options

    def run(self, folders):
        """Read snf output file and run turbomole calculations
        for every vibration mode. Calculation is controlled via 'input.json'

        Args:
            path (str): path to inputfiles ('snf.out' and 'input.json')
        """
        self.mode_folders = folders
        cwd = os.getcwd()
        os.chdir(self.options['workdir'])
        if self.options['sp_control']['qc_prog'] == 'turbomole':
            calcmanager.start_tm_single_points(folders, self.options)
        os.chdir(cwd)
