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
    """Small wrapper class to ASE-Atoms object.

    """
    def __init__(self, atoms=None, atomicnumbers=None, vectors=None):
        """Creates molecule from atoms and vectors.[Bohr]

        Parameters
        ----------
        atoms : :obj:`list` of :obj:`str`, optional
            List declaring the atom names.
        vectors : :obj:`list` of :obj:`float`, optional
            List declaring vectors of atoms
        atomicnumbers : :obj:`list` of :obj:`int`, optional
            List declaring atomic numbers.

        """
        self.atoms = atoms
        self.vectors = np.array(vectors, dtype=np.float64)
        self.an = atomicnumbers
        for idx, at in enumerate(self.atoms):
            self.atoms[idx] = self.atoms[idx][0] + self.atoms[idx][1:].lower()

    def to_ASE_atoms_obj(self):
        """Converts this class to ASE class.

        Returns
        -------
        :obj:`ASE-Atoms`

        """
        return Atoms(''.join(self.atoms),
                     [[idx*Bohr for idx in vec] for vec in self.vectors])

    def print(self):
        """Print atoms with corresping vectors

        """
        print('Printing molecule')
        assert len(self.atoms) == len(self.vectors) == len(self.an)
        for idx, atom in enumerate(self.atoms):
            print(atom, self.an[idx], self.vectors[idx])
