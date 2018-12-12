import os

from ase import io

from snfio import SnfParser
from molecule import Molecule


def writeDisortion(mode_idx, outformat, snfoutname='snf.out', delta=0.1):
    """TODO: to be defined1. """
    path = './'
    snfparser = SnfParser(snfoutname=snfoutname)
    molecule = snfparser.get_molecule()

    #  modes = snfparser.get_modes()
    #  for mode in modes:
    #
    #      pass

    mode0_vecs = snfparser.get_mode(0).vectors
    dissortions = [molecule.vectors - mode0_vecs*delta,
                   molecule.vectors + mode0_vecs*delta]

    asedissortions = [Molecule(molecule.atoms, vectors=dis).to_ASE_atoms_obj()
                      for dis in dissortions]

    os.chdir(path)
    for idx, dissortion in enumerate(asedissortions):
        modedir = 'mode0_' + str(idx)
        os.mkdir(modedir)
        os.chdir(modedir)
        io.write(dissortion.get_chemical_formula(mode='hill')
                 + '.' + str(outformat),
                 dissortion,
                 format=outformat)
        os.chdir('../')
