# PyIETS

# Postprocessing tool for calculating the IETS intensity and hence the
# electron-phonon-interaction
#
# Copyright (C) 2019 Benjamin Bolbrinker
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


import re
import numpy as np
from ase import io

import pyiets.atoms.vibration as vib
import pyiets.atoms.molecule as mol


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
        # counter = 0
        # for line in self.snfoutfile:
        # if 'root no.' in line:
        # lidx = counter
        # break
        # counter += 1
        # return len(np.fromstring(self.snfoutfile[lidx+2],
        # dtype=np.float, sep=' '))
        mode_idx_list = []
        for line in self.snfoutfile:
            if 'root no.' in line:
                mode_idx_list.append(
                        [i for i in re.findall(r'(\d*)', line) if i])
        return int(mode_idx_list[-1][-1])

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

    def _get_mode_vectors(self, mode_idx):
        begin_idx = None
        for idx, line in enumerate(self.snfoutfile):
            if re.search(r'root no\..*?\s('
                         + str(mode_idx + 1) + r')\s.*', line):
                begin_idx = idx
                break
        assert begin_idx is not None
        block_width = len(self.snfoutfile[begin_idx+2].split())
        wavenum = float(self.snfoutfile[begin_idx+2]
                        .split()[mode_idx % block_width])
        counter = 0
        block = []
        for line in self.snfoutfile[begin_idx+4:]:
            pline = re.findall(r'([+-]?(?:\d+\.\d+))', line)
            if line.isspace():
                break
            if len(pline) == block_width:
                block.append(float(pline[mode_idx % block_width]))
                counter += 1
                if counter is 3*self.natoms:
                    break
        assert len(block) is 3*self.natoms
        return wavenum, block

    def get_mode(self, mode_idx):
        """TODO: to be defined1. """
        wavenum, mode_vectors = self._get_mode_vectors(mode_idx)
        mode_vectors = np.array(mode_vectors).reshape(self.natoms, 3)
        mode = vib.Mode(vectors=mode_vectors,
                        atoms=self.molecule.atoms,
                        wavenumber=wavenum,
                        idx=mode_idx)
        return mode

        # wavenum = (np.fromstring(mode_block[2],
                   # dtype=np.float, sep=' ')[(mode_idx) % 6])
        # print(wavenum)
        # for idx, line in enumerate(self.snfoutfile):
            # # print(r'root no..*(' + str(mode_idx) + r').*\n')
            # if re.search(r'root no\..*?\s('
                         # + str(mode_idx + 1) + r')\s.*', line):
                # print('Test')
                # wavenum = (np.fromstring(self.snfoutfile[idx + 2],
                           # dtype=np.float, sep=' ')[(mode_idx) % 6])
                # for idx_2, line_2 in enumerate(self.snfoutfile[idx+4:], idx+4):
                    # if re.search(r'root no\.\s.*\n', line_2):
                        # raw_modes_str = self.snfoutfile[idx+4:idx_2]
                    # elif re.search(r'Generate fake outputs for normal mode pr',
                                   # line_2):
                        # raw_modes_str = self.snfoutfile[idx+4:idx_2]
                    # break
                # break
        # regex_float = r'[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?'
        # print(mode_idx, wavenum)
        # print(raw_modes_str)
        # raw_modes_string = [it.split()[3:] for it in raw_modes_str]
        # raw_modes_str = []
        # for vec in raw_modes_string:
            # if vec:
                # raw_modes_str.append(vec)
        # # print(raw_modes_str)
        # # print([it for it in raw_modes_str_list if re.match(regex_float, it)])
        # modes = list(map(lambda x: [float(st) for st in x], raw_modes_str))
        # modevectors = list(map(list, zip(*modes)))[(mode_idx + 1) % 6]
        # assert len(modevectors) % 3 == 0
        # modevectors = np.array(modevectors).reshape(int(len(modes)/3), 3)
        # mode = vib.Mode(vectors=modevectors,
                        # atoms=self.molecule.atoms,
                        # wavenumber=wavenum,
                        # idx=mode_idx)
        # return mode

             
                
                # break
        # counter = 0
        # for line in self.snfoutfile:
            # if 'root no.' in line:
                # lidx0 = counter
                # break
            # counter += 1

        # vibenergy = np.fromstring(self.snfoutfile[lidx0+2],
                                  # dtype=np.float, sep=' ')[idx]

        # raw_modes_str = [re.findall(r'\-?\d+\.\d+',
                                    # self.snfoutfile[lidx0+line_idx+4])
                         # for line_idx in range(3*self.natoms)]
        # modes = list(map(lambda x: [float(st) for st in x], raw_modes_str))
        # print(self.natoms)
        # modevectors = list(map(list, zip(*modes)))[idx]
        # assert len(modevectors) % 3 == 0
        # modevectors = np.array(modevectors).reshape(int(len(modes)/3), 3)
        # mode = vib.Mode(vectors=modevectors,
                        # atoms=self.molecule.atoms,
                        # wavenumber=vibenergy,
                        # idx=idx)
        # return mode

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
