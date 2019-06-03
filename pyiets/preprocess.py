import os
import ase.io
import pyiets.io.snfio
import pyiets.io.gaussianio
import pyiets.io.turbomoleio
import multiprocessing
from pyiets.atoms.molecule import Molecule
import numpy as np


class Preprocessor():
    def __init__(self, workdir, options):
        self.workdir = workdir
        self.options = options

        if options['vib_out'] == 'snf':
            self.parser = pyiets.io.snfio.Parser(options)
        elif options['vib_out'] == 'gaussian':
            self.parser = pyiets.io.gaussianio.Parser(options)
        elif options['vib_out'] == 'turbomole':
            self.parser = pyiets.io.turbomoleio.Parser(options)

        dissotionoutname = self.parser.get_molecule()\
            .to_ASE_atoms_obj().get_chemical_formula(mode='hill') + '.xyz'
        self.dissotionoutname = dissotionoutname
        options['dissotionoutname'] = dissotionoutname

    def preprocess(self):
        modes = self.options['modes']
        if modes == 'all':
            modes = self.parser.get_modes()
        else:
            modes = [self.parser.get_mode(int(mode_idx))
                     for mode_idx in modes]

        # chunksize = int(len(modes)/self.options['mp'])
        # if chunksize < 1:
            # chunksize += 1
        # with multiprocessing.Pool(processes=self.options['mp']) as pool:
            # modes_pool = pool.map(to_weighted, modes, chunksize=chunksize)
            # pool.close()
            # pool.join()

        # modes = [mode for mode in modes_pool]
        [mode.to_weighted() for mode in modes]

        if self.options['restart']:
            return (self._prepareDistortions(modes),
                    self.parser.get_molecule())
        else:
            return (self._writeDistortions(modes),
                    self.parser.get_molecule())

    def _prepareDistortions(self, modes):
        molecule = self.parser.get_molecule()
        for mode in modes:
            mode_vecs = np.array(mode.vectors, dtype=np.float64)
            dissortions = [molecule.vectors - mode_vecs*self.options['cstep'],
                           molecule.vectors + mode_vecs*self.options['cstep']]

            asedissortions = [Molecule(molecule.atoms, vectors=dis)
                              .to_ASE_atoms_obj()
                              for dis in dissortions]
            dissortion_folders = []
            for idx, dissortion in enumerate(asedissortions):
                modedir = 'mode' + str(mode.get_idx()) + '_' + str(idx)
                dissortion_folders.append(modedir)
                os.chdir('../')
            mode.set_folders(dissortion_folders)
        return modes

    def _writeDistortions(self, modes):
        cwd = os.getcwd()
        molecule = self.parser.get_molecule()

        os.makedirs(os.path.join(self.workdir, self.options['mode_folder']),
                    exist_ok=True)
        # os.mkdir(os.path.join(self.workdir, self.options['mode_folder']))
        outdirpath = os.path.abspath(os.path.join(self.workdir,
                                                  self.options['mode_folder']))

        returnarr = []
        spname = self.options['sp_name']
        returnarr.append(os.path.realpath(spname))
        os.chdir(outdirpath)
        os.makedirs(spname, exist_ok=True)
        # os.mkdir(spname)
        os.chdir(spname)
        ase.io.write(self.dissotionoutname,
                     molecule.to_ASE_atoms_obj(),
                     format="xyz")

        os.chdir('../../')

        for mode in modes:
            mode_vecs = np.array(mode.vectors, dtype=np.float64)
            # disstortion0 = []
            # for idx, vec in enumerate(molecule.vectors):
            # disstortion0 = np.array(vec) - np.array(mode_vecs[idx])

            dissortions = [molecule.vectors - mode_vecs*self.options['cstep'],
                           molecule.vectors + mode_vecs*self.options['cstep']]

            asedissortions = [Molecule(molecule.atoms, vectors=dis)
                              .to_ASE_atoms_obj()
                              for dis in dissortions]

            os.chdir(outdirpath)
            dissortion_folders = []
            for idx, dissortion in enumerate(asedissortions):
                modedir = 'mode' + str(mode.get_idx()) + '_' + str(idx)
                os.makedirs(modedir, exist_ok=True)
                # os.mkdir(modedir)
                dissortion_folders.append(modedir)
                os.chdir(modedir)
                ase.io.write(self.dissotionoutname,
                             dissortion,
                             format='xyz')
                os.chdir('../')
            mode.set_folders(dissortion_folders)

        os.chdir(cwd)
        returnarr.append(modes)
        return modes


def to_weighted(mode):
    mode.to_weighted()
    return mode
