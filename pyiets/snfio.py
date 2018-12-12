
import re
import numpy as np
from ase import io

import vibration as vib
import molecule as mol


class SnfParser:
    """Docstring for MyClass. """
    def __init__(self, snfoutname='snf.out'):
        """TODO: to be defined1. """
        self.snfoutname = snfoutname
        with open(self.snfoutname, 'r') as fp:
            self.snfoutfile = fp.readlines()
        self.natoms = self._get_natoms()
        self.nmodes = self._get_nmodes()
        self.molecule = self.get_molecule()

    def _get_natoms(self):
        """TODO: to be defined1. """
        natomline = [line for line in self.snfoutfile
                     if 'Number of atoms' in line]
        if len(set(natomline)) in [1]:
            line = natomline[0].strip().replace(' ', '')
            idx = re.search(r'\d+', line).start()
            natomstr = line[idx:]
            return int(natomstr)
        elif len(set(natomline)) in [0]:
            raise Exception('No number of atoms provided in {}'
                            .format(self.snfoutname))
        else:
            raise Exception('Ambiguous number of atoms provided in {}'
                            .format(self.snfoutname))

    def _get_nmodes(self):
        """TODO: to be defined1. """
        counter = 0
        for line in self.snfoutfile:
            if 'root no.' in line:
                lidx = counter
                break
            counter += 1
        return len(np.fromstring(self.snfoutfile[lidx+2],
                                 dtype=np.float, sep=' '))

    def get_molecule(self):
        """TODO: to be defined1. """
        counter = 0
        for line in self.snfoutfile:
            if 'Molecule of snf run' in line:
                lidx0 = counter
            if 'Restart file information' in line:
                lidx1 = counter
                break
            counter += 1
        moleculestring = self.snfoutfile[lidx0:lidx1]
        moleculestring = moleculestring[4:-1]

        atoms = [atomstring.split()[1] for atomstring in moleculestring]
        moleculestring = [atomstring.split()[4:]
                          for atomstring in moleculestring]

        molecvectors = [[float(i) for i in vec] for vec in moleculestring]
        molec = mol.Molecule(atoms=atoms, vectors=molecvectors)
        return molec

    def get_mode(self, idx):
        """TODO: to be defined1. """
        counter = 0
        for line in self.snfoutfile:
            if 'root no.' in line:
                lidx0 = counter
                break
            counter += 1

        vibenergy = np.fromstring(self.snfoutfile[lidx0+2],
                                  dtype=np.float, sep=' ')[idx]

        raw_modes_str = [re.findall(r'\-?\d+\.\d+',
                                    self.snfoutfile[lidx0+line_idx+4])
                         for line_idx in range(3*self.natoms)]
        modes = list(map(lambda x: [float(st) for st in x], raw_modes_str))
        modevectors = list(map(list, zip(*modes)))[idx]
        assert len(modevectors) % 3 == 0
        modevectors = np.array(modevectors).reshape(int(len(modes)/3), 3)
        mode = vib.Mode(vectors=modevectors,
                        atoms=self.molecule.atoms,
                        wavenumber=vibenergy)
        return mode

    def get_modes(self):
        """TODO: to be defined1. """
        modes = []
        for idx in range(self.nmodes):
            modes.append(self.get_mode(idx))
        assert len(modes) == self.nmodes
        return modes


def exportMolecule(snfoutname, outformat):
    """TODO: to be defined1. """
    snfparser = SnfParser(snfoutname=snfoutname)
    molecule = snfparser.get_molecule()
    asemolecule = molecule.to_ASE_atoms_obj()
    io.write(asemolecule.get_chemical_formula(mode='hill')
             + '.' + str(outformat),
             asemolecule,
             format=outformat)
