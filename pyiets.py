#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import pyiets.io.snfio
import pyiets.io.createInput
import pyiets.io.parseInput
import pyiets.runcalcs.calcmanager as calcmanager
import pyiets.io.checkinput


def pyiets_run(path):
    """Run pyiets
    Args:
        path (str): path to inputfiles
    """
    defaults_parser = pyiets.io.parseInput.InputParser('default_settings.json')
    options = defaults_parser.getSinglePointOptions()

    os.chdir(path)
    inparser = pyiets.io.parseInput.InputParser(options['input_file'])
    options.update(inparser.getSinglePointOptions())
    pyiets.io.checkinput.check_options(options)

    snfparser = pyiets.io.snfio.SnfParser(snfoutname=options['snf_out'])
    dissotionoutname = snfparser.get_molecule().to_ASE_atoms_obj() \
        .get_chemical_formula(mode='hill') + '.' + str(
            options['sp_control']['qc_prog'])

    if not os.path.exists(options['mode_folder']):
        pyiets.io.createInput.writeDisortion(dissotionoutname,
                                             options['mode_folder'],
                                             options['sp_control']['qc_prog'],
                                             options['snf_out'],
                                             delta=0.1)

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


if __name__ == '__main__':
    pyiets_run(sys.argv[1])
