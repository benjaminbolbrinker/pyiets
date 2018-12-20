#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import json
import pyiets.io.snfio
import pyiets.io.createInput
import pyiets.runcalcs.calcmanager as calcmanager
import pyiets.io.checkinput


def read_input(inputfilename):
    with open(inputfilename, 'r') as infile:
        indata = json.load(infile)
    return indata


def pyiets_run(path):
    """Run pyiets
    Args:
        path (str): path to inputfiles
    """
    options = read_input('input_defaults.json')
    os.chdir(path)
    options.update(options['input_file'])
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
