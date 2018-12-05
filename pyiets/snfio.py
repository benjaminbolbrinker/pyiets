
import re
import numpy as np

import vibration as vib



class snfParser:
    def __init__(self, snfoutname='snf.out'):
        self.snfoutname = snfoutname
        with open(self.snfoutname, 'r') as fp:
            self.snfoutfile = fp.readlines()
        self.natoms = self._get_natoms()
        self.nmodes = self._get_nmodes()

    def _get_natoms(self):
        natomline = [line for line in self.snfoutfile
                     if 'Number of atoms' in line]
        if len(set(natomline)) in [1]:
            line = natomline[0].strip().replace(' ', '')
            idx = re.search('\d+', line).start()
            natomstr = line[idx:]
            return int(natomstr)
        elif len(set(natomline)) in [0]:
            raise Exception('No number of atoms provided in {}'
                            .format(self.snfoutname))
        else:
            raise Exception('Ambiguous number of atoms provided in {}'
                            .format(self.snfoutname))

    def _get_nmodes(self):
        counter = 0
        for line in self.snfoutfile:
            if 'root no.' in line:
                lidx = counter
                break
            counter += 1
        return len(np.fromstring(self.snfoutfile[lidx+2],
                                 dtype=np.float, sep=' '))

    def get_molecule(self):
        counter = 0
        for line in self.snfoutfile:
            if 'Molecule of snf run' in line:
                lidx0 = counter
            if 'Restart file information' in line:
                lidx1 = counter
                break
            counter += 1
        modelines = self.snfoutfile[lidx0:lidx1]
        return modelines

    def get_mode(self, idx):
        counter = 0
        for line in self.snfoutfile:
            if 'root no.' in line:
                lidx0 = counter
                break
            counter += 1
        lidx1 = lidx0 + 4 + 3 * self.natoms

        vibenergy = np.fromstring(self.snfoutfile[lidx0+2],
                                  dtype=np.float, sep=' ')[idx]
        modecolidx = re.search('\number', line).start()

        return modecolidx
        #  return vibenergy
        #  return self.snfoutfile[lidx0:lidx1]


    def get_modes(self):
        modes = []
        for idx in range(self.nmodes):
            modes.append(self._get_mode(idx))
        assert len(modes) == self.nmodes
        return modes
