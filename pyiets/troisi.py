import os
import math
from shutil import copyfile, move
import numpy as np
from tempfile import mkstemp


class Troisi:
    def __init__(self, options, modes, greenmat_dictarr):
        self.options = options
        self.modes = modes
        self.greenmat_dictarr = greenmat_dictarr
        self.troisi_greenmatrices = []
        self.output_mode_folders = [None]*len(modes)

    def calc_greensmatrix(self, mode_idx):
        mode = self.modes[mode_idx]
        cstep = 1
        gm_idx = [[g for g in self.greenmat_dictarr
                  if mode.get_folders()[idx] == g['mode']][0]
                  for idx in range(len(mode.get_folders()))]
        sp_gm = next(g for g in self.greenmat_dictarr
                     if g['mode'] == 'sp')
        d0 = self.options['delta']

        troisi_greenmatrix = (math.sqrt(2*d0)/(2*d0) * (0.5*d0/cstep) *
                              (np.array(gm_idx[1]['greensmatrix'])
                              - np.array(sp_gm['greensmatrix'])))
        self.modes[mode_idx].set_troisi_greensmat(gm=troisi_greenmatrix)

    def _init_output(self):
        for mode in self.modes:
            folder = os.path.join(self.options['workdir'],
                                  self.options['output_folder'],
                                  self.options['output_mode_folder_prefix']
                                  + str(mode.get_idx()))
            self.output_mode_folders[mode.get_idx()] = folder
            os.makedirs(folder, exist_ok=True)
            copyfile(os.path.join(self.options['workdir'],
                     self.options['artaios_in']),
                     os.path.join(folder, self.options['artaios_in']))
            self._change_for_read(os.path.join(folder,
                                               self.options['artaios_in']))

    def _change_for_read(self, artaios_in):
        # Create temp file
        fh, abs_path = mkstemp()
        with os.fdopen(fh, 'w') as fp:
            with open(artaios_in) as old_file:
                for line in old_file:
                    fp.write(line.replace('print_green', 'read_green'))
        os.remove(artaios_in)
        move(abs_path, artaios_in)
        pass

    def write_troisi_greensmatrix(self, mode):
        with open(os.path.join(self.options['workdir'],
                  self.output_mode_folders[mode.get_idx()],
                  self.options['troisi_greenmatrix_file']), 'w') as fp:
            gm = self.troisi_greenmatrices[mode.get_idx()]
            for row in gm:
                for c in row:
                    fp.write('(' + str(c.real) + ',' + str(c.imag) + ')')
                fp.write('\n')


    def prepare_input_artaios(self):
        self._init_output()
        for mode in self.modes:
            self.write_troisi_greensmatrix(mode)

    def calc_greensmatrices(self):
        troisi_mat = []
        for mode in self.modes:
            self.calc_greensmatrix(mode.get_idx())
            troisi_mat.append(mode.get_troisi_greensmat())
        self.troisi_greenmatrices = troisi_mat

    def read_green_artatios_for_mode(self, idx):
        return self.modes[idx]

    def read_green_artatios(self):
        [self.read_green_artatios_for_mode(mode.idx)
         for mode in self.modes]

    def calc_IET_spectrum(self):
        self.prepare_input_artaios()

    # def calc_IETS_intensity_for(self, mode_idx):
        # pass

    def print_IET_spectrum(self):
        pass
