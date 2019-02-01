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

import numpy as np


class Mode:
    """Docstring for MyClass. """
    def __init__(self, vectors=None, atoms=None, wavenumber=None, idx=None,
                 dissortion_folders=None, troisi_greensmatrix=None):
        """TODO: to be defined1. """
        self.vectors = np.array(vectors)
        self.atoms = atoms
        self.wavenumber = wavenumber
        self.idx = idx
        self.dissortion_folders = dissortion_folders

        self.troisi_greensmatrix = troisi_greensmatrix
        self.iets = []

    def set_troisi_greensmat(self, gm):
        """TODO: to be defined1. """
        self.troisi_greensmatrix = gm

    def get_troisi_greensmat(self):
        """TODO: to be defined1. """
        return self.troisi_greensmatrix

    def set_iets(self, iets):
        """TODO: to be defined1. """
        self.iets = iets

    def get_iets(self):
        """TODO: to be defined1. """
        return self.iets

    def set_wavenumber(self, wn):
        """TODO: to be defined1. """
        self.wavenumber = wn

    def get_wavenumber(self):
        """TODO: to be defined1. """
        return self.wavenumber

    def set_atoms(self, stringarr):
        """TODO: to be defined1. """
        self.atoms = stringarr

    def get_atoms(self):
        """TODO: to be defined1. """
        return self.atoms

    def set_vectors(self, matrix_3bynatm):
        """TODO: to be defined1. """
        self.vectors = matrix_3bynatm

    def get_vectors(self):
        """TODO: to be defined1. """
        return self.vectors

    def set_folders(self, folder_str_list):
        """TODO: to be defined1. """
        self.dissortion_folders = folder_str_list

    def get_folders(self):
        """TODO: to be defined1. """
        return self.dissortion_folders

    def set_idx(self, idx):
        """TODO: to be defined1. """
        self.idx = idx

    def get_idx(self):
        """TODO: to be defined1. """
        return self.idx

    def print(self):
        """TODO: to be defined1. """
        print('Printing mode:', self.idx)
        print('Wavenumber:', self.wavenumber)
        assert len(self.atoms) == len(self.vectors)
        for idx, atom in enumerate(self.atoms):
            print(atom, self.vectors[idx])
        print('Folders:', self.dissortion_folders)
