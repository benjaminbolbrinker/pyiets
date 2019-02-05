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
import re
import multiprocessing

import pyiets.runcalcs.calcmanager as calcmanager


class Artaios():
    def __init__(self, workdir, options):
        self.workdir = workdir
        self.options = options
        self.greenmatrices = None
        self.mode_folders = None

    def run(self, mode_folders):
        """Read tm mos files and run artaios calculations
        for every vibration mode. Calculation is controlled via 'input.json'

        Args:
            path (str): path to inputfiles ('artaios.in' and 'input.json')
                        and mode_folder containing previously
                        calculated single points corresponding to different
                        normal-modes.
        """
        cwd = os.getcwd()
        os.chdir(self.workdir)
        self.mode_folders = mode_folders

        if self.options['sp_control']['qc_prog'] == 'turbomole':
            calcmanager.start_artaios(mode_folders,
                                      self.options)

        os.chdir(cwd)

    def read_greenmatrices(self):
        with multiprocessing.Pool(processes=self.options['mp']) as pool:
            # files = [str(os.path.join(folder,
            # self.options['greenmatrix_file']))
            # for folder in self.mode_folders]
            # greenmatrices = pool.imap(self.read_greenmatrix, files)
            greenmatrices = [self.read_greenmatrix(str(os.path.join(folder,
                             self.options['greenmatrix_file'])))
                             for folder in self.mode_folders]
            pool.close()
            pool.join()

        return [matrix for matrix in greenmatrices]

    def read_greenmatrix(self, greenmatrixfile):
        # with open(greenmatrixfile, 'r') as greenfile:
            # dim = int(greenfile.readline())
        with open(greenmatrixfile, 'r') as greenfile:
            rawinput = greenfile.readlines()[1:]

        line = rawinput[0]
        # floating_point = r'[-+]?\d+[.][Ee0-9+-]+'
        # greenmatrix = np.empty(shape=(dim, dim), dtype=np.complex)
        greenmatrix = []
        for idx, line in enumerate(rawinput):
            # arr = re.findall('[(] *' + floating_point + ' *, *' +
            # floating_point + ' *[)]', line)
            # arr = [np.fromstring(rawcomplex
            # .replace('(', '')
            # .replace(')', ''), sep=', ').tolist()
            # for rawcomplex in arr]
            arr = [[float(a[0]), float(a[1])]
                   for a in re.findall(r'\(\s*(.*?)\s*,\s*(.*?)\s*\)', line)]
            arr = [complex(*a) for a in arr]
            # print(arr)
            # print(arr, greenmatrixfile)
            # np.insert(greenmatrix, idx, arr, axis=1)
            greenmatrix.append(arr)
        folder, fn = os.path.split(greenmatrixfile)
        return {'mode': os.path.basename(folder),
                'greensmatrix': greenmatrix}
