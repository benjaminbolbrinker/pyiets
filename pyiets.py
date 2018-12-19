#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import pyiets.io.snfio
import pyiets.io.createInput
import pyiets.io.parseInput
import pyiets.runcalcs.calcmanager as calcmanager


def pyiets_run():
    defaults_parser = pyiets.io.parseInput.InputParser('default_settings.json')
    options = defaults_parser.getSinglePointOptions()
    os.chdir(sys.argv[1])
    inparser = pyiets.io.parseInput.InputParser(options['input_file'])
    options.update(inparser.getSinglePointOptions())
    restartfile = pyiets.io.createInput.create_ascending_name(
        options['restart_file'])

    snfparser = pyiets.io.snfio.SnfParser(snfoutname=options['snf_out'])
    dissotionoutname = snfparser.get_molecule().to_ASE_atoms_obj() \
        .get_chemical_formula(mode='hill') + '.' + str(
            options['sp_control']['qc_prog'])

    if options['restart']:
        folder = pyiets.io.createInput.find_descending_dirname('./')
        if 'folder' in options:
            folder = options['folder']
        if options['mp'] > 0:
            calcmanager.restart_tm_single_points(folder, options,
                                                 options['mp'], restartfile)
        else:
            pyiets.io.parseInput._wrongInputErrorMessage(options['mp'],
                                                         options['input_file'])
    else:
        outfolder = pyiets.io.createInput.create_ascending_name(
            options['mode_folder'])
        if 'folder' in options:
            outfolder = pyiets.io.createInput \
                        .create_ascending_name(options['folder'])
        pyiets.io.createInput.writeDisortion(dissotionoutname, outfolder,
                                             options['sp_control']['qc_prog'],
                                             options['snf_out'], delta=0.1)
        if options['mp'] > 0:
            calcmanager.start_tm_single_points(outfolder, options,
                                               options['mp'], restartfile)
        else:
            pyiets.io.parseInput._wrongInputErrorMessage(options['mp'],
                                                         options['infile'])


if __name__ == '__main__':
    pyiets_run()
