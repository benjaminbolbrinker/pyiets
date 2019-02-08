import os
import math
from shutil import copyfile, move
import numpy as np
from tempfile import mkstemp

import pyiets.artaios as artaios
import pyiets.atoms.vibration as vib


class Troisi:
    def __init__(self, options, modes, greenmat_dictarr):
        self.options = options
        self.modes = vib.Modes(modes)
        self.greenmat_dictarr = greenmat_dictarr
        self.troisi_greenmatrices = []
        self.output_mode_folders = [None]*len(modes)
        self.iets_dict_list = None

    def calc_greensmatrix(self, mode_idx):
        # print(mode_idx, self.modes)
        # mode = self.modes[mode_idx]
        mode = self.modes.find_by(mode_idx)

        cstep = 1
        gm_idx = [[g for g in self.greenmat_dictarr
                  if mode.get_folders()[idx] == g['mode']][0]
                  for idx in range(len(mode.get_folders()))]
        # sp_gm = next(g for g in self.greenmat_dictarr
        # if g['mode'] == 'sp')
        d0 = self.options['delta']

        troisi_greenmatrix = (math.sqrt(2*d0)/(2*d0) * (0.5*d0/cstep) *
                              (np.array(gm_idx[1]['greensmatrix'])
                              - np.array(gm_idx[0]['greensmatrix'])))
        mode.set_troisi_greensmat(gm=troisi_greenmatrix)

    def _init_output(self, path_to_sp):
        for idx, mode in enumerate(self.modes):
            folder = os.path.join(self.options['workdir'],
                                  self.options['output_folder'],
                                  self.options['output_mode_folder_prefix']
                                  + str(mode.get_idx()))
            self.output_mode_folders[idx] = folder
            os.makedirs(folder, exist_ok=True)

            # copyfile(os.path.join(self.options['workdir'],
            # self.options['artaios_in']),
            # os.path.join(folder, self.options['artaios_in']))
            sp_files = []
            for f in os.listdir(path_to_sp):
                if (os.path.isfile(os.path.join(path_to_sp, f))
                   and f != self.options['greenmatrix_file']
                   and f != self.options['artaios_stdout']
                   and f != self.options['artaios_stderr']):
                    sp_files.append(f)
            for f in sp_files:
                copyfile(os.path.join(path_to_sp, f), os.path.join(folder, f))
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

    def write_troisi_greensmatrix(self, mode, folder_idx):
        with open(os.path.join(self.options['workdir'],
                  self.output_mode_folders[folder_idx],
                  self.options['troisi_greenmatrix_file']), 'w') as fp:
            gm = self.troisi_greenmatrices[folder_idx]
            assert len(gm) == len(gm[0])
            fp.write(str(len(gm)) + '\n')
            for row in gm:
                for c in row:
                    fp.write(' ( ' + str(c.real) + ' , ' + str(c.imag) + ' ) ')
                fp.write('\n')

    def prepare_input_artaios(self):
        self._init_output(os.path.join(self.options['workdir'],
                                       self.options['mode_folder'], 'sp'))
        for idx, mode in enumerate(self.modes):
            self.write_troisi_greensmatrix(mode, idx)

    def calc_greensmatrices(self):
        troisi_mat = []
        for mode in self.modes.modes:
            self.calc_greensmatrix(mode.get_idx())
            troisi_mat.append(mode.get_troisi_greensmat())
        self.troisi_greenmatrices = troisi_mat
        return troisi_mat

    def calc_IET_spectrum(self):
        self.prepare_input_artaios()
        art = artaios.Artaios(
              os.path.join(self.options['workdir'],
                           self.options['output_folder']), self.options)
        # folders = set([os.path.realpath(f.path) for f in
        # os.scandir(os.path.join(
        # self.options['workdir'],
        # self.options['output_folder']))
        # if f.is_dir()])
        folders = [os.path.join(self.options['workdir'],
                                self.options['output_folder'],
                                self.options['output_mode_folder_prefix'])
                   + str(mode.get_idx())
                   for mode in self.modes]
        art.run(folders)
        iets_dict_list = []
        for idx, mode in enumerate(self.modes):
            iets_dict_list.append({
                'mode': self.modes[idx],
                'transmission': art.read_transmission_for(
                    os.path.join(folders[idx], self.options['artaios_stdout'])
                    )
                })
        self.iets_dict_list = iets_dict_list
        return iets_dict_list

    def write_IET_spectrum(self, filename):
        if self.iets_dict_list is not None:
            with open(filename, 'w') as fp:
                for d in self.iets_dict_list:
                    # fp.write('Mode' + str(d['mode'].get_idx()) + '\n')
                    # fp.write('Wavenumber: '
                    # + str(d['mode'].get_wavenumber()) + 'cm-1\n')
                    # fp.write('-'*30 + '\n')
                    for e_t_pair in d['transmission']:
                        fp.write(str(d['mode'].get_idx()) + ' ' +
                                 str(d['mode'].get_wavenumber()) + ' ' +
                                 ' '.join(map(str, e_t_pair)) + '\n')
                    # fp.write('-'*30 + '\n')
                    # fp.write('-'*30 + '\n')
                    # fp.write('\n')
