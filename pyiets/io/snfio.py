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
import os
import numpy as np
from ase import io

import pyiets.atoms.vibration as vib
import pyiets.atoms.molecule as mol

from mendeleev import element


class Parser:
    """Class for parsing snf output in options['vib_out_file'] file.

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
        self.snfoutname = os.path.join(options['workdir'], options['vib_out_file'])
        with open(self.snfoutname, 'r') as fp:
            self.snfoutfile = fp.readlines()
        self.natoms = self._get_natoms()
        self.nmodes = self._get_nmodes()
        self.molecule = self.get_molecule()
        self.options['cstep'] = self._get_distortion()

    def _get_natoms(self):
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
        mode_idx_list = []
        for line in self.snfoutfile:
            if 'root no.' in line:
                mode_idx_list.append(
                        [i for i in re.findall(r'(\d*)', line) if i])
        return int(mode_idx_list[-1][-1])

    def _get_distortion(self):
        """ Get disstortion length. Defaults to 0.01 Bohr.

        Returns
        -------
        float
            Distortion length in Bohr.

        """
        regex = (r'\s*distortion\s\[bohr\]\s*:\s*([+-]?\d*.\d*)\s*')
        cstep_search = None
        for line in self.snfoutfile:
            cstep_search = re.search(regex, line)
            if cstep_search:
                break
        if cstep_search:
            cstep = float(cstep_search.group(1))
        else:
            cstep = 0.01
            print('Disstortion not found in {}'
                  .format(self.options['snf_out']))
            print('Setting cstep to 0.010 Bohr (default)')
        return cstep

    def get_molecule(self):
        """ Get molecule specified in options['snf_out'].

        Parameters
        ----------
        mode_idx : :obj:`int`
            index of mode.

        Returns
        -------
        :obj:`list` of :obj:`pyiets.atoms.atoms.Molecule`
            Molecule object

        """
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
        an = [int(atomstring.split()[2]) for atomstring in moleculestring]
        moleculestring = [atomstring.split()[4:]
                          for atomstring in moleculestring]

        molecvectors = [[float(i) for i in vec] for vec in moleculestring]
        molec = mol.Molecule(atoms=atoms, atomicnumbers=an,
                             vectors=molecvectors)
        return molec

    def _get_mode_vectors(self, mode_idx):
        """ Get vector of the (mode_idx + 1)-th mode in options['snf_out'].

        Parameters
        ----------
        mode_idx : :obj:`int`
            index of mode.

        Returns
        -------
        :obj:`tuple`
            Contains wavenumber and raw coordinate vectors of mode.

        """
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
        """ Get (mode_idx + 1)-th mode in options['snf_out'].

        Parameters
        ----------
        mode_idx : :obj:`int`
            index of mode.

        Returns
        -------
        :obj:`pyiets.atoms.vibration.Mode`
            Mode object

        """
        wavenum, mode_vectors = self._get_mode_vectors(mode_idx)
        mode_vectors = np.array(mode_vectors,
                                dtype=np.float64).reshape(self.natoms, 3)
        isotope_masses = [np.float64(self.options['isotope_masses']
                          [str(element(m).atomic_number)]
                          [str(element(m).mass_number)]
                          ['mass']) for m in self.molecule.atoms]
        mode = vib.Mode(vectors=mode_vectors,
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


def exportMolecule(snfoutname, outformat):
    snfparser = Parser(snfoutname=snfoutname)
    molecule = snfparser.get_molecule()
    asemolecule = molecule.to_ASE_atoms_obj()
    io.write(asemolecule.get_chemical_formula(mode='hill')
             + '.' + str(outformat),
             asemolecule,
             format=outformat)
