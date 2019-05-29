import os
import logging
import pyiets.atoms.molecule as mol
import pyiets.atoms.vibration as vib
import numpy as np

import cclib

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
        self.turbomoleoutname = os.path.join(options['workdir'],
                                             options['vib_out_file'])
        parser = cclib.io.ccopen(self.turbomoleoutname,
                                 loglevel=logging.WARNING)
        self.data = parser.parse()
        self.natoms = self._get_natoms()
        self.nmodes = self._get_nmodes()
        self.molecule = self.get_molecule()
        self.options['cstep'] = self._get_distortion()

    def _get_natoms(self):
        return self.data.natom

    def _get_nmodes(self):
        return len(self.data.vibfreqs)

    def _get_distortion(self):
        return self.options['cstep']

    def get_molecule(self):
        atomicnumbers = self.data.atomnos
        atomnames = [element(int(i)).symbol for i in atomicnumbers.tolist()]
        vectors = [[i/Bohr for i in l]
                   for l in next(iter(self.data.atomcoords.tolist()))]

        molec = mol.Molecule(atoms=atomnames,
                             atomicnumbers=atomicnumbers.tolist(),
                             vectors=vectors)
        return molec

    def get_mode(self, mode_idx):
        isotope_masses = [np.float64(self.options['isotope_masses']
                          [str(element(m).atomic_number)]
                          [str(element(m).mass_number)]
                          ['mass']) for m in self.molecule.atoms]
        mode = vib.Mode(vectors=self.data.vibdisps[mode_idx],
                        atoms=self.molecule.atoms,
                        wavenumber=self.data.vibfreqs[mode_idx],
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
