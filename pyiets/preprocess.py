import os
import ase.io
import pyiets.io.snfio
from pyiets.atoms.molecule import Molecule


class Preprocessor():
    def __init__(self, workdir, options):
        self.workdir = workdir
        self.options = options
        snf_parser = pyiets.io.snfio.SnfParser(options)
        self.snf_parser = snf_parser
        dissotionoutname = snf_parser.get_molecule()\
            .to_ASE_atoms_obj().get_chemical_formula(mode='hill') + '.' + str(
            options['sp_control']['qc_prog'])
        self.dissotionoutname = dissotionoutname
        options['dissotionoutname'] = dissotionoutname

    def preprocess(self):
        modes = self.options['modes']
        if modes == 'all':
            modes = self.snf_parser.get_modes()
        else:
            modes = [self.snf_parser.get_mode(int(mode_idx))
                     for mode_idx in modes]

        if self.options['sp_restart']:
            return self._prepareDistortions(modes)
        else:
            return self._writeDistortions(modes)

    def _prepareDistortions(self, modes):
        molecule = self.snf_parser.get_molecule()
        for mode in modes:
            mode_vecs = mode.vectors
            dissortions = [molecule.vectors - mode_vecs*self.options['delta'],
                           molecule.vectors + mode_vecs*self.options['delta']]

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
        molecule = self.snf_parser.get_molecule()

        os.mkdir(os.path.join(self.workdir, self.options['mode_folder']))
        outdirpath = os.path.abspath(os.path.join(self.workdir,
                                                  self.options['mode_folder']))

        returnarr = []
        spname = self.options['sp_name']
        returnarr.append(os.path.realpath(spname))
        os.chdir(outdirpath)
        os.mkdir(spname)
        os.chdir(spname)
        ase.io.write(self.dissotionoutname,
                     molecule.to_ASE_atoms_obj(),
                     format=self.options['sp_control']['qc_prog'])

        os.chdir('../../')

        for mode in modes:
            mode_vecs = mode.vectors
            dissortions = [molecule.vectors - mode_vecs*self.options['delta'],
                           molecule.vectors + mode_vecs*self.options['delta']]

            asedissortions = [Molecule(molecule.atoms, vectors=dis)
                              .to_ASE_atoms_obj()
                              for dis in dissortions]

            os.chdir(outdirpath)
            dissortion_folders = []
            for idx, dissortion in enumerate(asedissortions):
                modedir = 'mode' + str(mode.get_idx()) + '_' + str(idx)
                os.mkdir(modedir)
                dissortion_folders.append(modedir)
                os.chdir(modedir)
                ase.io.write(self.dissotionoutname,
                             dissortion,
                             format=self.options['sp_control']['qc_prog'])
                os.chdir('../')
            mode.set_folders(dissortion_folders)

        os.chdir(cwd)
        returnarr.append(modes)
        return modes
