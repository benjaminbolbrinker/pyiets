import os
import ase.io
import pyiets.io.snfio
from pyiets.atoms.molecule import Molecule


class Preprocessor():
    def __init__(self, workdir, options):
        self.workdir = workdir
        self.options = options
        snf_parser = pyiets.io.snfio.SnfParser(
            os.path.join(self.workdir, self.options['snf_out'])
        )
        self.snf_parser = snf_parser
        dissotionoutname = snf_parser.get_molecule()\
            .to_ASE_atoms_obj().get_chemical_formula(mode='hill') + '.' + str(
            options['sp_control']['qc_prog'])
        self.dissotionoutname = dissotionoutname
        options['dissotionoutname'] = dissotionoutname

    def writeDisortion(self):
        cwd = os.getcwd()
        molecule = self.snf_parser.get_molecule()
        dissortion_folders = []

        modes = self.snf_parser.get_modes()
        os.mkdir(os.path.join(self.workdir, self.options['mode_folder']))
        outdirpath = os.path.abspath(os.path.join(self.workdir,
                                                  self.options['mode_folder']))
        for mode_idx, mode in enumerate(modes):
            mode_vecs = self.snf_parser.get_mode(mode_idx).vectors
            dissortions = [molecule.vectors - mode_vecs*self.options['delta'],
                           molecule.vectors + mode_vecs*self.options['delta']]

            asedissortions = [Molecule(molecule.atoms, vectors=dis)
                              .to_ASE_atoms_obj()
                              for dis in dissortions]

            os.chdir(outdirpath)
            for idx, dissortion in enumerate(asedissortions):
                modedir = 'mode' + str(mode_idx) + '_' + str(idx)
                os.mkdir(modedir)
                dissortion_folders.append(modedir)
                os.chdir(modedir)
                ase.io.write(self.dissotionoutname,
                             dissortion,
                             format=self.options['sp_control']['qc_prog'])
                os.chdir('../')

        os.chdir(cwd)
