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
import numpy as np

import pyiets.runcalcs.calcmanager as calcmanager


class Artaios():
    def __init__(self, mode_folders, options, restartsaveloc=None):
        """Class for starting artaios transport calculations in mode_folders.

        Note
        ----
        Set at least options['workdir'], options['sp_control'],
                     options['qc_prog'], options['greenmatrixfile'],
                     options['artaios'], options['artaios_bin'],
                     options['artaios_in'], options[artaios_restart_file'],
                     options['artaios_stdout'], options['artaios_stderr']

        Parameters
        ----------
        mode_folders : :obj:`list` of :obj:`str`
            contains paths to folders with inputfiles ('artaios.in'
            and 'input.json') and previously successfully
            finished single point calculations corresponding
            to different normal-modes.
        """
        self.options = options
        self.mode_folders = mode_folders
        self.restartsaveloc = restartsaveloc
        self.greenmatrices = None

    def preprocess(self):
        """Read turbomole mos-files and run artaios calculations
        for every vibration mode. Mos-filename has to be specisfied in
        options['artaios_in'] file. Calculation is controlled via 'input.json'

        Note
        ----
        Set at least options['workdir'], options['sp_control'],
                     options['qc_prog'], options['artaios'],
                     options['artaios_bin'], options['artaios_in'],
                     options[artaios_restart_file'], options['artaios_stdout'],
                     options['artaios_stderr']

        """
        cwd = os.getcwd()
        os.chdir(self.options['workdir'])
        if self.options['sp_control']['qc_prog'] == 'turbomole':
            if self.options['tcc']:
                calcmanager.start_tm2unformsoc(self.mode_folders,
                                               self.options,
                                               self.restartsaveloc)
            else:
                calcmanager.start_tm2unformcl(self.mode_folders,
                                              self.options,
                                              self.restartsaveloc)
        if self.options['sp_control']['qc_prog'] == 'gaussian':
            calcmanager.start_g092unform(self.mode_folders,
                                         self.options, self.restartsaveloc)

        os.chdir(cwd)

    def run(self):
        """Read turbomole mos-files and run artaios calculations
        for every vibration mode. Mos-filename has to be specisfied in
        options['artaios_in'] file. Calculation is controlled via 'input.json'

        Note
        ----
        Set at least options['workdir'], options['sp_control'],
                     options['qc_prog'], options['artaios'],
                     options['artaios_bin'], options['artaios_in'],
                     options[artaios_restart_file'], options['artaios_stdout'],
                     options['artaios_stderr']

        """
        cwd = os.getcwd()
        os.chdir(self.options['workdir'])

        calcmanager.start_artaios(self.mode_folders,
                                  self.options,
                                  self.restartsaveloc)

        os.chdir(cwd)

    def read_greenmatrices(self, files):
        """Call after self.run(). Read greeanmatrices from files.

        Parameters
        ----------
        files : :obj:`list` of :obj:`str`
            contains absoulte paths specifying the greensmatrix files from
            artaios-output to be read.
        """
        return [self.read_greenmatrix(f) for f in files]
        # with multiprocessing.Pool(processes=self.options['mp']) as pool:
        # greenmatrices = pool.imap(self.read_greenmatrix, files)
        # pool.close()
        # pool.join()

        # return [matrix for matrix in greenmatrices]

    def read_greenmatrix(self, greenmatrixfile):
        """Call after self.run(). Read greeanmatrix from files.

        Parameters
        ----------
        greenmatrixfile : :obj:`str`
            contains absoulte path specifying the greensmatrix file from
            artaios-output to be read.
        """
        with open(greenmatrixfile, 'r') as greenfile:
            rawinput = greenfile.readlines()[1:]

        line = rawinput[0]
        greenmatrix = []
        for idx, line in enumerate(rawinput):
            arr = [[float(a[0]), float(a[1])]
                   for a in re.findall(r'\(\s*(.*?)\s*,\s*(.*?)\s*\)', line)]
            arr = [np.complex128(complex(*a)) for a in arr]
            greenmatrix.append(arr)
        folder, fn = os.path.split(greenmatrixfile)
        return {'mode': os.path.basename(folder),
                'greensmatrix': greenmatrix}

    def read_transmission_for(self, artaios_out):
        """Call after self.run(). Read transmission from artaios
        std-output.

        Parameters
        ----------
        artaios_out : :obj:`str`
            contains absoulte path specifying a file containing
            artaios-std-output to be read.
        """
        with open(artaios_out, 'r') as fp:
            rawinput = fp.readlines()
        if self.options['tcc']:
            regex = r'\s*(?:([+-]?\d+\.\d+(?:[eEdD][+-]\d+)?)\s+)'*6
            transmission_list = []
            for idx, line in enumerate(rawinput):
                arr = [[float(a[0]), float(a[1]), float(a[2]),
                        float(a[3]), float(a[4]), float(a[5])]
                       for a in re.findall(regex, line)]
                [transmission_list.append(a) for a in arr if a]

        else:
            float_re = r'[-+]?\d+[.][Ee0-9+-]+'
            regex = (r'energy;\s*transmission:\s*(' +
                     float_re + r')\s*(' +
                     float_re + r')')
            transmission_list = []
            for idx, line in enumerate(rawinput):
                arr = [[float(a[0]), float(a[1])]
                       for a in re.findall(regex, line)]
                [transmission_list.append(a) for a in arr if a]
        return transmission_list

    def read_transmission(self):
        """Call after self.run(). Read all transmission from artaios
        std-output for all self.mode_folders

        Note
        ----
        Set at least options['greenmatrixfile']

        Returns
        -------
        :obj:`list`
            containing the transmissions.
        """
        # files = [str(os.path.join(folder,
                 # self.options['greenmatrix_file']))
                 # for folder in self.mode_folders]
        # return [self.read_transmission_for(f) for f in files]
        with multiprocessing.Pool(processes=self.options['mp']) as pool:
            files = [str(os.path.join(folder,
                     self.options['greenmatrix_file']))
                     for folder in self.mode_folders]
            transmission = pool.imap(self.read_transmission_for, files)
            pool.close()
            pool.join()

        return [matrix for matrix in transmission]
