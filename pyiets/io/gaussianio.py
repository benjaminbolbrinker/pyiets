import os
import re

import cclib
from mendeleev import element
from ase.units import Bohr

import pyiets.atoms.vibration as vib
import pyiets.atoms.molecule as mol


class Parser:
    def __init__(self, options):
        self.options = options
        self.gaussianoutname = os.path.join(options['workdir'],
                                            options['vib_out_file'])
        with open(self.gaussianoutname, 'r') as fp:
            self.gaussianoutfile = fp.readlines()
        self.data = cclib.io.ccread(self.gaussianoutname)
        self.natoms = self._get_natoms()
        self.nmodes = self._get_nmodes()
        self.molecule = self.get_molecule()
        self.options['cstep'] = self._get_distortion()

    def _get_distortion(self):
        return 0.01

    def _get_natoms(self):
        return self.data.natom

    def _get_nmodes(self):
        return len(self.data.vibdisps)

    def get_molecule(self):
        for idx, line in enumerate(self.gaussianoutfile):
            if (re.search(r'\s*Standard orientation:\s*', line) and
               re.search(r'\s-+\s*', self.gaussianoutfile[idx+1]) and
               re.search(r'\s*Center\s*Atomic\s*Atomic\s*Coordinates\s*'
               + r'\(Angstroms\)\s*', self.gaussianoutfile[idx+2]) and
               re.search(r'\s-+\s*', self.gaussianoutfile[idx+4])):
                break
        idx += 5
        raw_block = []
        while not re.search(r'\s-{5,}\s*', self.gaussianoutfile[idx]):
            raw_block.append(self.gaussianoutfile[idx].split())
            idx += 1
        an = [int(line[1]) for line in raw_block]
        vectors = [[float(i)/Bohr for i in line[3:6]] for line in raw_block]
        atomnames = [element(i).symbol for i in an]

        molec = mol.Molecule(atoms=atomnames, atomicnumbers=an,
                             vectors=vectors)
        return molec

    def get_mode(self, mode_idx):
        return vib.Mode(vectors=self.data.vibdisps[mode_idx],
                        atoms=self.get_molecule().atoms,
                        wavenumber=self.data.vibfreqs[mode_idx],
                        idx=mode_idx)

    def get_modes(self):

        """ Get all modes written in option['snf_out'].

        Note
        ----
        Indexing begins with 0!

        Returns
        -------
        :obj:`list` of :obj:`pyiets.atoms.vibration.Mode`
            Mode object

        """
        modes = []
        if self.options['modes'] == 'all':
            for mode_idx in range(self.nmodes):
                modes.append(self.get_mode(mode_idx))
        else:
            for mode_idx in self.options['modes']:
                modes.append(self.get_mode(int(mode_idx)))
        assert len(modes) == self.nmodes
        return modes
