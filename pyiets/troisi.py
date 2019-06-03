import os
import math
from shutil import copyfile, move
import numpy as np
from tempfile import mkstemp
import multiprocessing

import pyiets.artaios as artaios
import pyiets.restart as restart


class Troisi:
    ''' Class for calculating the IETS intensity from previous single
    point and transport calculations.
    '''
    def __init__(self, options, modes, greenmat_dictarr, molecule):
        """ Constructor of SinglePoint class.
        Note
        ----
        Set at least options['greenmatrix'], options['outfolder'],
                     options['greenmatrix_file'], options['artaios_stdout'],
                     options['artaios_stderr'], options'[artaios_in'],
                     options['artaios'], options['aratios_bin'],
                     options['workdir'], options['output_folder'],
                     options['output_mode_folder_prefix'],
                     options['troisi_greenmatrix_file']


        Parameters
        ----------
        options : :obj:`dict`
            Dict containing the relevant parameters.
        modes : :obj:`list` of :obj:`pyiets.atoms.vibration.Mode`
            List of folders to start single point calculation in.
        greenmat_dictarr : :obj:`dict` of :obj:`str` and :obj:`list` of float
            Dict containing modefolder names and corresponding greenmatrix

        """
        self.options = options
        self.modes = modes
        self.greenmat_dictarr = greenmat_dictarr
        self.molecule = molecule
        self.troisi_greenmatrices = []
        self.output_mode_folders = [None]*len(modes)
        self.iets_dict_list = None

    def calc_greensmatrix(self, mode_idx):
        """Calculate the greensfunction of the (mode_idx + 1)-th mode
        in options['snf_out'].

        Note
        ----
        Set at least options['greenmatrix']

        Parameters
        ----------
        mode_idx : int
            Number specifying the index of the mode to calculate in
            options['snf_out']. Note that the indexing starts from 0.

        """
        mode = next((mode for mode in self.modes
                    if mode.get_idx() == mode_idx), None)

        cstep = self.options['cstep']

        gm_idx = [[g for g in self.greenmat_dictarr
                  if mode.get_folders()[idx] == g['mode']][0]
                  for idx in range(len(mode.get_folders()))]

        reduced_mass = 0.0
        mode.to_non_weighted()
        assert len(mode.get_vectors()) == len(self.molecule.an)
        for idx, vector in enumerate(mode.get_vectors()):
            for coord in vector:
                # reduced_mass += np.float64((np.float64(coord)**2)/(np.float64(
                # element(self.molecule.an[idx]).atomic_weight)))
                reduced_mass += np.float64((np.float64(coord)**2)/(np.float64(
                    mode.isotope_masses[idx]
                    )))
        reduced_mass = np.float64(1.0) / (reduced_mass)
        troisi_greenmatrix = (((math.sqrt(2.0)/(4.0))/cstep) *
                              (np.array(gm_idx[1]['greensmatrix'],
                               dtype=np.complex128)
                              - np.array(gm_idx[0]['greensmatrix'],
                               dtype=np.complex128)))
        troisi_greenmatrix /= math.sqrt(reduced_mass)
        if self.options['verbose']:
            mode.print()
            print(gm_idx[0])
            print(gm_idx[1])
            print(troisi_greenmatrix)
        mode.set_troisi_greensmat(gm=troisi_greenmatrix)
        return troisi_greenmatrix

    def _init_output(self, path_to_sp):
        """Initialises input for reading artaios calculation.
        in options['snf_out'].

        Note
        ----
        Set at least options['greenmatrix'], options['outfolder'],
                     options['greenmatrix_file'], options['artaios_stdout'],
                     options['artaios_stderr'], options'[artaios_in'],
                     options['artaios'], options['aratios_bin'],
                     options['workdir'], options['output_folder'],
                     options['output_mode_folder_prefix']

        Parameters
        ----------
        path_to_sp : :obj:`str`
            Path to previous single point calculation.

        """
        for idx, mode in enumerate(self.modes):
            folder = os.path.join(self.options['workdir'],
                                  self.options['output_folder'],
                                  self.options['output_mode_folder_prefix']
                                  + str(mode.get_idx()))
            self.output_mode_folders[idx] = folder
            os.makedirs(folder, exist_ok=True)

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
        """Changes artaios_in file to read greenmatrix instead of print.

        Parameters
        ----------
        path_to_sp : :obj:`str`
            Path to artatios.in file.

        """
        # Create temp file
        fh, abs_path = mkstemp()
        with os.fdopen(fh, 'w') as fp:
            with open(artaios_in) as old_file:
                for line in old_file:
                    fp.write(line.replace('print_green', 'read_green'))
        os.remove(artaios_in)
        move(abs_path, artaios_in)

    def write_troisi_greensmatrix(self, mode, folder_idx):
        """Writes troisi greensfunction to file.

        Note
        ----
        Set at least options['troisi_greenmatrix_file']

        Parameters
        ----------
        mode : :obj:`pyiets.atoms.vibration.Mode`
            Mode to write greensfunction for.
        folder_idx : int
            Index of folder

        """
        with open(os.path.join(self.options['workdir'],
                  self.output_mode_folders[folder_idx],
                  self.options['troisi_greenmatrix_file']), 'w') as fp:
            gm = self.troisi_greenmatrices[folder_idx]
            assert len(gm) == len(gm[0])
            fp.write(str(len(gm)) + '\n')
            for row in gm:
                for c in row:
                    fp.write(' ( %.14e , %.14e ) ' % (c.real, c.imag))
                fp.write('\n')

    def prepare_input_artaios(self):
        """Prepares input fore upcoming transport calculation.

        Note
        ----
        Set at least options['workdir'], options['mode_folder']

        """
        self._init_output(os.path.join(self.options['workdir'],
                                       self.options['mode_folder'], 'sp'))
        for idx, mode in enumerate(self.modes):
            self.write_troisi_greensmatrix(mode, idx)

    def calc_greensmatrices(self):
        """Calculates Troisi Greensmatrix.

        Returns
        -------
        :obj:`list`
            Troisi Greensmatrix.

        """
        troisi_mat = []
        for mode in self.modes:
            self.calc_greensmatrix(mode.get_idx())
            troisi_mat.append(mode.get_troisi_greensmat())
        self.troisi_greenmatrices = troisi_mat
        return troisi_mat

        # with multiprocessing.Pool(processes=self.options['mp']) as pool:
            # troisi_mat = pool.map(self.calc_greensmatrix,
                                  # [mode.get_idx() for mode in self.modes])
            # pool.close()
            # pool.join()

        # self.troisi_greenmatrices = [t for t in troisi_mat]
        # return self.troisi_greenmatrices

    def calc_IET_spectrum(self):
        """Calculates IETS.

        Note
        ----
        Set at least options['greenmatrix'], options['outfolder'],
                     options['greenmatrix_file'], options['artaios_stdout'],
                     options['artaios_stderr'], options'[artaios_in'],
                     options['artaios'], options['aratios_bin'],
                     options['workdir'], options['output_folder'],
                     options['output_mode_folder_prefix'],
                     options['troisi_greenmatrix_file']

        Returns
        -------
        :obj:`dict`
            Dict containing information about the iets spectrum.

        """
        self.prepare_input_artaios()
        folders, done = restart.choose_mode_folders(
                os.path.join(self.options['workdir'],
                             self.options['output_folder'],
                             self.options['artaios_restart_file']),
                os.path.join(self.options['workdir'],
                             self.options['output_folder']),
                self.options['restart']
                )
        art = artaios.Artaios(folders, self.options,
                              restartsaveloc=self.options['output_folder'])
        art.preprocess()
        art.run()
        iets_dict_list = []
        for idx, mode in enumerate(self.modes):
            iets_dict_list.append({
                'mode': self.modes[idx],
                'transmission': art.read_transmission_for(
                    os.path.join(self.output_mode_folders[idx],
                                 self.options['artaios_stdout'])
                    )
                })
        self.iets_dict_list = iets_dict_list
        return iets_dict_list

    def write_IET_spectrum(self, filename):
        """Writes IETS.

        Parameters
        ----------
        filename : :obj:`str`
            path of file to write.

        """
        if self.iets_dict_list is not None:
            with open(filename, 'w') as fp:
                for d in self.iets_dict_list:
                    for e_t_pair in d['transmission']:
                        fp.write(str(d['mode'].get_idx()) + ' ' +
                                 str(d['mode'].get_wavenumber()) + ' ' +
                                 ' '.join(map(str, e_t_pair)) + '\n')
