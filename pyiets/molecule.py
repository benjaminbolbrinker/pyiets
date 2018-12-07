class Molecule:
    def __init__(self, atoms=None, vectors=None):
        self.atoms = atoms
        self.vectors = vectors
    def print(self):
        print('Printing molecule')
        assert len(self.atoms) == len(self.vectors)
        for idx, atom in enumerate(self.atoms):
            print(atom, self.vectors[idx])


