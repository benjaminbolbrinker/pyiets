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
import pyiets.runcalcs.calcmanager as calcmanager


class SinglePoint():
    '''Wrapper class to select quantum chemistry program.

    Options dictionary defines parameters how program should behave.
    Each function requires different key-value pairs to be set.
    A single point calculation is started in each folder provided.
    Restartability may also be provided by setting a restartfile,
    which saved folders which already have been calculated as plain
    string separated by spaces.

    '''

    def __init__(self, mode_folders, options, restartsaveloc=None):
        """ Constructor of SinglePoint class

        Note
        ----
        Set at least options['sp_control'], options['sp_control']['params'],
                     options['qc_prog'], options['workdir'],
                     options['dissotionoutname'], options['sp_restart']

        Parameters
        ----------
        mode_folders : :obj:`list` of :obj:`str`
            List of folders to start single point calculation in.
        options : :obj:`dict`
            Dict containing the relevant parameters.
        restartsaveloc : :obj:`str`, optional
            Path to restartfile.

        """
        self.options = options
        self.mode_folders = mode_folders
        self.restartsaveloc = restartsaveloc

    def run(self):
        """Run single calculations in every folder provided in
        contructor.

        Note
        ----
        Set at least options['sp_control'], options['sp_control']['params'],
                     options['qc_prog'], options['workdir'],
                     options['dissotionoutname'], options['sp_restart']

        """
        cwd = os.getcwd()
        os.chdir(self.options['workdir'])
        if self.options['sp_control']['qc_prog'] == 'turbomole':
            calcmanager.start_tm_single_points(self.mode_folders, self.options,
                                               self.restartsaveloc)
        elif self.options['sp_control']['qc_prog'] == 'gaussian':
            calcmanager.start_gaussian_single_points(self.mode_folders,
                                                     self.options,
                                                     self.restartsaveloc)
        os.chdir(cwd)
