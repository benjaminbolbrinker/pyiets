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
from ase import Atoms
from ase.units import Bohr


class Molecule:
    """Docstring for MyClass. """
    def __init__(self, atoms=None, vectors=None):
        """TODO: to be defined1. """
        self.atoms = atoms
        self.vectors = np.array(vectors)
        for idx, at in enumerate(self.atoms):
            self.atoms[idx] = self.atoms[idx][0] + self.atoms[idx][1:].lower()

    def to_ASE_atoms_obj(self):
        """TODO: to be defined1. """
        return Atoms(''.join(self.atoms),
                     [[idx*Bohr for idx in vec] for vec in self.vectors])

    def print(self):
        """TODO: to be defined1. """
        print('Printing molecule')
        assert len(self.atoms) == len(self.vectors)
        for idx, atom in enumerate(self.atoms):
            print(atom, self.vectors[idx])
