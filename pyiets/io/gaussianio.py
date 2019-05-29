import os
import re
import pyiets.atoms.molecule as mol
import pyiets.atoms.vibration as vib
import numpy as np

from ase.units import Bohr

from mendeleev import element


class Parser:
    """Class for parsing options['snf_out'] file.

    """
    def __init__(self, options):
        """ Creates parser object.

        Note
        ----
        Relevant parameters are...

        Parameters
        ----------
        options : :obj:`dict`
            dict to set behaviour.

        """
        self.options = options
        self.gaussianoutname = os.path.join(options['workdir'],
                                            options['vib_out_file'])
        with open(self.gaussianoutname, 'r') as fp:
            self.gaussianoutfile = fp.readlines()
        self.natoms = self._get_natoms()
        self.nmodes = self._get_nmodes()
        self.molecule = self.get_molecule()
        self.options['cstep'] = self._get_distortion()

    def _get_natoms(self):
        for idx, line in enumerate(self.gaussianoutfile):
            if (re.search(r'\s*Standard orientation:\s*', line) and
               re.search(r'\s-+\s*', self.gaussianoutfile[idx+1]) and
               re.search(r'\s*Center\s*Atomic\s*Atomic\s*Coordinates\s*'
               + r'\(Angstroms\)\s*', self.gaussianoutfile[idx+2]) and
               re.search(r'\s-+\s*', self.gaussianoutfile[idx+4])):
                break
        idx += 5
        idx2 = idx

        while not re.search(r'\s-{5,}\s*', self.gaussianoutfile[idx2]):
            idx2 += 1
        natoms = idx2 - idx
        return natoms

    def _get_nmodes(self):
        for idx1, line in enumerate(self.gaussianoutfile):
            if re.search(r'Harmonic\sfrequencies', line):
                break

        nblocks = 0
        ncols = []
        for idx2, line in enumerate(self.gaussianoutfile[idx1:], idx1):
            if re.search(r'\s*Atom\s*AN\s+', line):
                ncols.append(len(re.findall(r'(X\s{2,}Y\s{2,}Z)', line)))
                nblocks += 1
        assert len(ncols) == nblocks

        nmodes = sum(ncols)
        return nmodes

    def _get_distortion(self):
        return self.options['cstep']

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

    def _get_wavenumbersabove(self, idx):
        while not re.search(r'Frequencies --', self.gaussianoutfile[idx]):
            idx -= 1
        return [float(i) for i in re.findall(r'[+-]?\d+\.\d+',
                                             self.gaussianoutfile[idx])]

    def get_mode(self, mode_idx):

        for idx1, line in enumerate(self.gaussianoutfile):
            if re.search(r'Harmonic\sfrequencies', line):
                break

        nblocks = 0
        for idx2, line in enumerate(self.gaussianoutfile[idx1:], idx1):
            if re.search(r'\s*Atom\s*AN\s+', line):
                ncols = len(re.findall(r'(X\s+Y\s+Z)', line))
                nblocks += 1
        column = mode_idx % ncols
        block_idx = 0
        for idx2, line in enumerate(self.gaussianoutfile[idx1:], idx1):
            if re.search(r'\s*Atom\s*AN\s+', line):
                wavenum = self._get_wavenumbersabove(idx2)[column]
                if block_idx == int(mode_idx/ncols):
                    raw_block = []
                    for idx3, line in enumerate(self.gaussianoutfile[idx2+1:],
                                                idx2):
                        if re.search(r'\d+\s+\d+(\s+[-+]?\d+\.\d+)+', line):
                            raw_block.append(line)
                        else:
                            break
                    assert len(raw_block) == self.natoms
                    break
                block_idx += 1
        vector_block = [[float(i) for i in
                        l.split()[2:][column*3:(column*3)+3]]
                        for l in raw_block]

        isotope_masses = [np.float64(self.options['isotope_masses']
                          [str(element(m).atomic_number)]
                          [str(element(m).mass_number)]
                          ['mass']) for m in self.molecule.atoms]
        mode = vib.Mode(vectors=vector_block,
                        atoms=self.molecule.atoms,
                        wavenumber=wavenum,
                        idx=mode_idx,
                        weighted=True,
                        isotope_masses=isotope_masses)
        return mode

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
