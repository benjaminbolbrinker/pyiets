
class Mode:
    def __init__(self, vectors=None, atoms=None, wavenumber=None):
        self.vectors = vectors
        self.atoms = atoms
        self.wavenumber = wavenumber

    def set_wavenumber(self, wn):
        self.wavenumber = wn

    def set_atoms(self, stringarr):
        self.atoms = stringarr

    def set_vectors(self, matrix_3bynatm):
        self.vectors = matrix_3bynatm

    def get_wavenumber(self):
        return self.wavenumber

    def get_atoms(self):
        return self.atoms

    def get_vectors(self):
        return self.vectors

    def print(self):
        print('Printing mode...')
        print('Wavenumber:', self.wavenumber)
        assert len(self.atoms) == len(self.get_vectors)
        for idx, atom in enumerate(self.atoms):
            print(atom, self.vectors[idx])
