from ase import Atoms
from ase.units import Bohr

class Molecule:
    """Docstring for MyClass. """
    def __init__(self, atoms=None, vectors=None):
        """TODO: to be defined1. """
        self.atoms = atoms
        self.vectors = vectors

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
