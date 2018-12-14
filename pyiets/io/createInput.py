import os

from ase import io

from pyiets.io.snfio import SnfParser
from pyiets.atoms.molecule import Molecule


outdir = 'dissortions'


def createOutDir_ascending(outdirname):
    if not os.path.exists(outdirname):
        os.mkdir(outdirname)
        return outdirname
    else:
        i = 0
        while os.path.exists(outdirname + '{}'.format(i)):
            i += 1
        dirname = outdirname + '{}'.format(i)
        os.mkdir(dirname)
        return dirname


def writeDisortion(outformat, snfoutname='snf.out', delta=0.1):
    """TODO: to be defined1. """
    cwd = os.getcwd() + '/'
    snfparser = SnfParser(snfoutname=snfoutname)
    molecule = snfparser.get_molecule()

    modes = snfparser.get_modes()

    outdirpath = createOutDir_ascending(cwd + outdir)
    for mode_idx, mode in enumerate(modes):
        mode_vecs = snfparser.get_mode(mode_idx).vectors
        dissortions = [molecule.vectors - mode_vecs*delta,
                       molecule.vectors + mode_vecs*delta]

        asedissortions = [Molecule(molecule.atoms, vectors=dis)
                          .to_ASE_atoms_obj()
                          for dis in dissortions]

        os.chdir(outdirpath)
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
