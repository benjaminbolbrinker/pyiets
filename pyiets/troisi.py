import math
import numpy as np


class Troisi:
    def __init__(self, options, modes, greenmat_dictarr):
        self.options = options
        self.modes = modes
        self.greenmat_dictarr = greenmat_dictarr
        self.troisi_greenmatrices = []

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
        print(troisi_greenmatrix)
        greensmatrix = None
        self.modes[mode_idx].set_troisi_greensmat(gm=greensmatrix)

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
