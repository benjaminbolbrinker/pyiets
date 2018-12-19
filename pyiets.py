#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import pyiets.io.snfio
import pyiets.io.createInput
import pyiets.io.parseInput
import pyiets.runcalcs.calcmanager as calcmanager
import pyiets.io.checkinput


def pyiets_run():
    """TODO: to be defined1. """
    defaults_parser = pyiets.io.parseInput.InputParser('default_settings.json')
    options = defaults_parser.getSinglePointOptions()
    os.chdir(sys.argv[1])
    inparser = pyiets.io.parseInput.InputParser(options['input_file'])
    options.update(inparser.getSinglePointOptions())
    pyiets.io.checkinput.check_options(options)

    snfparser = pyiets.io.snfio.SnfParser(snfoutname=options['snf_out'])
    dissotionoutname = snfparser.get_molecule().to_ASE_atoms_obj() \
        .get_chemical_formula(mode='hill') + '.' + str(
            options['sp_control']['qc_prog'])

    if options['restart']:
        if options['sp_control']['qc_prog'] == 'turbomole':
            if os.path.exists(options['restart_file']):
                with open(options['restart_file'], 'r') as restartfile:
                    mode_folders = set([f.path for f in
                                        os.scandir(options['mode_folder'])
                                        if f.is_dir()]) \
                                   - set(restartfile.read().split())
                    calcmanager.start_tm_single_points(mode_folders,
                                                       options['sp_control'],
                                                       options['mp'],
                                                       options['restart_file'])

    else:
        outfolder = pyiets.io.createInput.\
            create_ascending_name(options['mode_folder'])
        restartfile = pyiets.io.createInput.create_ascending_name(
            options['restart_file'])
        pyiets.io.createInput.writeDisortion(dissotionoutname, outfolder,
                                             options['sp_control']['qc_prog'],
                                             options['snf_out'],
                                             delta=0.1)
        if options['sp_control']['qc_prog'] == 'turbomole':
            mode_folders = {f.path for f in os.scandir(options['mode_folder'])
                            if f.is_dir()}
            calcmanager.start_tm_single_points(mode_folders,
                                               options['sp_control'],
                                               options['mp'],
                                               restartfile)


if __name__ == '__main__':
    pyiets_run()
