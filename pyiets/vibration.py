import numpy as np


class Mode:
    """Docstring for MyClass. """
    def __init__(self, vectors=None, atoms=None, wavenumber=None):
        """TODO: to be defined1. """
        self.vectors = np.array(vectors)
        self.atoms = atoms
        self.wavenumber = wavenumber

    def set_wavenumber(self, wn):
        """TODO: to be defined1. """
        self.wavenumber = wn

    def set_atoms(self, stringarr):
        """TODO: to be defined1. """
        self.atoms = stringarr

    def set_vectors(self, matrix_3bynatm):
        """TODO: to be defined1. """
        self.vectors = matrix_3bynatm

    def get_wavenumber(self):
        """TODO: to be defined1. """
        return self.wavenumber

    def get_atoms(self):
        """TODO: to be defined1. """
        return self.atoms

    def get_vectors(self):
        """TODO: to be defined1. """
        return self.vectors

    def print(self):
        """TODO: to be defined1. """
        print('Printing mode...')
        print('Wavenumber:', self.wavenumber)
        assert len(self.atoms) == len(self.vectors)
        for idx, atom in enumerate(self.atoms):
            print(atom, self.vectors[idx])
