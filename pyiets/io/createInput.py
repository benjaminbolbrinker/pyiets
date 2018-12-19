import os

from ase import io

from pyiets.io.snfio import SnfParser
from pyiets.atoms.molecule import Molecule

outdir = ''


def create_ascending_name(name):
    """TODO: to be defined1. """
    if not os.path.exists(name):
        return name
    else:
        i = 0
        while os.path.exists(name + '{}'.format(i)):
            i += 1
        dirname = name + '{}'.format(i)
        return dirname


def find_descending_dirname(path):
    """TODO: to be defined1. """
    folders = [os.path.join(path, o) for o in os.listdir(path)
               if os.path.isdir(os.path.join(path, o))]
    return folders


def writeDisortion(outname, outfolder, outformat,
                   snfoutname='snf.out', delta=0.1):
    """TODO: to be defined1. """
    cwd = os.getcwd()
    snfparser = SnfParser(snfoutname=snfoutname)
    molecule = snfparser.get_molecule()
    dissortion_folders = []

    modes = snfparser.get_modes()
    os.mkdir(outfolder)
    outdirpath = os.path.abspath(outfolder)
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
            dissortion_folders.append(modedir)
            os.chdir(modedir)
            io.write(outname,
                     dissortion,
                     format=outformat)
            os.chdir('../')
    os.chdir(cwd)
    return dissortion_folders
