import os
import pyiets.io.snfio
import pyiets.io.createInput
import pyiets.runcalcs.calcmanager as calcmanager
import pyiets.io.checkinput
import pyiets.read


def run(path, options):
    """Read snf output file and run turbomole calculations
    for every vibration mode. Calculation is controlled via 'input.json'

    Args:
        path (str): path to inputfiles ('snf.out' and 'input.json')
    """
    cwd = os.getcwd()
    os.chdir(path)

    snfparser = pyiets.io.snfio.SnfParser(snfoutname=options['snf_out'])
    dissotionoutname = snfparser.get_molecule().to_ASE_atoms_obj() \
        .get_chemical_formula(mode='hill') + '.' + str(
            options['sp_control']['qc_prog'])

    if not os.path.exists(options['mode_folder']):
        pyiets.io.createInput.writeDisortion(dissotionoutname,
                                             options['mode_folder'],
                                             options['sp_control']['qc_prog'],
                                             options['snf_out'],
                                             delta=options['delta'])

    if os.path.exists(options['restart_file']):
        with open(options['restart_file'], 'r') as restartfile:
            mode_folders = set([f.path for f in
                                os.scandir(options['mode_folder'])
                                if f.is_dir()]) \
                            - set(restartfile.read().split())
    else:
            mode_folders = set([f.path for f in
                                os.scandir(options['mode_folder'])
                                if f.is_dir()])

    if options['sp_control']['qc_prog'] == 'turbomole':
        calcmanager.start_tm_single_points(mode_folders,
                                           dissotionoutname,
                                           options['sp_control']['params'],
                                           options['mp'],
                                           options['restart_file'])
    os.chdir(cwd)
