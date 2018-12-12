import os

from ase import io

from snfio import SnfParser
from molecule import Molecule


def writeDisortion(outformat, snfoutname='snf.out', delta=0.1):
    """TODO: to be defined1. """
    cwd = os.getcwd() + '/'
    snfparser = SnfParser(snfoutname=snfoutname)
    molecule = snfparser.get_molecule()

    modes = snfparser.get_modes()
    outdir = 'dissortions'
    os.mkdir(cwd + outdir)
    for mode_idx, mode in enumerate(modes):
        mode_vecs = snfparser.get_mode(mode_idx).vectors
        dissortions = [molecule.vectors - mode_vecs*delta,
                       molecule.vectors + mode_vecs*delta]

        asedissortions = [Molecule(molecule.atoms, vectors=dis)
                          .to_ASE_atoms_obj()
                          for dis in dissortions]

        os.chdir(cwd + outdir)
        for idx, dissortion in enumerate(asedissortions):
            modedir = 'mode' + str(mode_idx) + '_' + str(idx)
            os.mkdir(modedir)
            os.chdir(modedir)
            io.write(dissortion.get_chemical_formula(mode='hill')
                     + '.' + str(outformat),
                     dissortion,
                     format=outformat)
            os.chdir('../')
    os.chdir(cwd)
