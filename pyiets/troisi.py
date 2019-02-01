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
                  if mode.get_folders()[idx] == g['mode']]
                  for idx in range(len(mode.get_folders()))]
        sp_gm = next(g for g in self.greenmat_dictarr
                     if g['mode'] == 'sp')
        d0 = self.options['delta']
        print(math.sqrt(2*d0)/(2*d0) *
              (0.5*d0/cstep)*(np.array(gm_idx[1]['greensmatrix']) - np.array(gm_idx[0]['greensmatrix'])))
        # troisi_greenmatrix = math.sqrt
        greensmatrix = None
        self.modes[mode_idx].set_troisi_greensmat(gm=greensmatrix)

    def calc_greensmatrices():
        pass

    def read_green_artatios_for_mode(self, idx):
        return self.modes[idx]

    def read_green_artatios(self):
        [self.read_green_artatios_for_mode(mode.idx)
         for mode in self.modes]
