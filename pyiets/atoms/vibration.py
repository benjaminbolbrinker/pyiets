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

import math
import numpy as np


class Mode:
    """Small class to process information of vibrational modes.

    """
    def __init__(self, vectors, atoms, wavenumber, idx=None,
                 dissortion_folders=None, troisi_greensmatrix=None,
                 weighted=True, isotope_masses=None):
        """Creates vibrational mode.

        Parameters
        ----------
        vectors : :obj:`list` of :obj:`float`, optional
            List declaring vectors of atoms
        atoms : :obj:`list` of :obj:`str`, optional
            List declaring the atom names.
        wavenumber : float
            Wavenumber of mode.
        idx : int
            Index of mode.
        dissortion_folders : :obj:`list` of :obj:`str`
            folders containing dissorted vibration.
        troisi_greensmatrix : :obj:`list` of floats
            greensmatrix from Troisi ansatz

        """
        self.vectors = np.array(vectors, dtype=np.float64)
        self.atoms = atoms
        assert len(self.vectors) == len(self.atoms)
        self.wavenumber = wavenumber
        self.idx = idx
        self.dissortion_folders = dissortion_folders

        self.troisi_greensmatrix = troisi_greensmatrix
        self.iets = []
        self.weighted = weighted
        self.isotope_masses = isotope_masses
        # if options:
            # self.isotope_masses = [np.float64(options['isotope_masses']
                                   # [str(element(m).atomic_number)]
                                   # [str(element(m).mass_number)]
                                   # ['mass']) for m in atoms]

    def to_weighted(self):
        if not self.weighted:
            if self.isotope_masses:
                self.vectors = np.array([
                        [np.float64(i)/math.sqrt(self.isotope_masses[idx])
                         for i in vec]
                        for idx, vec in enumerate(self.vectors)], dtype=np.float64)
                # self.vectors = [self._normalize(vec) for vec in self.vectors]
            norm = np.linalg.norm(
                    np.reshape(self.vectors, int(len(self.vectors)*3)))

            if norm < 1e-9:
                norm = 1

            self.vectors /= norm
            self.weighted = True

    def to_non_weighted(self):
        # # if self.weighted:
            # self.vectors = np.array([
                    # [float(i)*math.sqrt(
                        # element(self.atoms[idx]).atomic_weight)
                     # for i in vec]
                    # for idx, vec in enumerate(self.vectors)], dtype=np.float64)
            # # # self.vectors = [self._normalize(vec) for vec in self.vectors]
            # norm = np.linalg.norm(
                    # np.reshape(self.vectors, int(len(self.vectors)*3)))

            # if norm < 1e-9:
                # norm = 1

            # self.vectors /= norm
            # # self.weighted = False
        if self.weighted:
            if self.isotope_masses:
                self.vectors = np.array([
                        [np.float64(i)*math.sqrt(self.isotope_masses[idx])
                         for i in vec]
                        for idx, vec in enumerate(self.vectors)], dtype=np.float64)
                # self.vectors = [self._normalize(vec) for vec in self.vectors]
            norm = np.linalg.norm(
                    np.reshape(self.vectors, int(len(self.vectors)*3)))

            if norm < 1e-9:
                norm = 1

            self.vectors /= norm
            self.weighted = False

    def set_troisi_greensmat(self, gm):
        """Set Greensfunction from Troisi ansatz.

        Parameters
        -------
        gm : :obj:`list` of floats

        """
        self.troisi_greensmatrix = gm

    def get_troisi_greensmat(self):
        """Get Greensfunction from Troisi ansatz.

        Returns
        -------
        :obj:`list` of floats

        """
        return self.troisi_greensmatrix

    def set_iets(self, iets):
        """Set IETS from Troisi ansatz.

        Parameters
        -------
        iets : :obj:`dict`

        """
        self.iets = iets

    def get_iets(self):
        """Get IETS from Troisi ansatz.

        Returns
        -------
        :obj:`dict`

        """
        return self.iets

    def set_wavenumber(self, wn):
        """Set wavenumber of modes.

        Parameters
        -------
        wn : float
            wavenumber in cm-1

        """
        self.wavenumber = wn

    def get_wavenumber(self):
        """Get wavenumber of modes.

        Returns
        -------
        float
            wavenumber in cm-1

        """
        return self.wavenumber

    def set_atoms(self, stringarr):
        """Set atoms

        Parameters
        -------
        stringarr : :obj:`list` of strings
            contains atom names.

        """
        self.atoms = stringarr

    def get_atoms(self):
        """Get atoms

        Returns
        -------
        :obj:`list` of strings
            contains atom names.

        """
        return self.atoms

    def set_vectors(self, matrix_3bynatm):
        """Set atom vectors

        Parameters
        -------
        matrix_3bynatm : :obj:`list` of strings
            contains atom vectors.

        """
        self.vectors = matrix_3bynatm

    def get_vectors(self):
        """Get atom vectors

        Returns
        -------
        :obj:`list` of floats
            contains atom vectors.

        """
        return self.vectors

    def set_folders(self, folder_str_list):
        """Set mode folders

        Parameters
        -------
        folder_str_list : :obj:`list` of strings
            paths to mode folders

        """
        self.dissortion_folders = folder_str_list

    def get_folders(self):
        """Get mode folders

        Returns
        -------
        :obj:`list` of strings
            paths to mode folders

        """
        return self.dissortion_folders

    def set_idx(self, idx):
        """Set mode index.

        Parameters
        -------
        idx : int

        """
        self.idx = idx

    def get_idx(self):
        """Get mode index

        Returns
        -------
        int

        """
        return self.idx

    def print(self):
        """Print mode.

        """
        print('Printing mode:', self.idx)
        print('Wavenumber:', self.wavenumber)
        assert len(self.atoms) == len(self.vectors)
        for idx, atom in enumerate(self.atoms):
            print(atom, self.vectors[idx])
        print('Folders:', self.dissortion_folders)
