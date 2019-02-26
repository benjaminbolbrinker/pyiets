#!/usr/bin/env python3

import os
import sys
import json

import pyiets.read

WORKDIR = sys.argv[1]

ROOT_DIR = os.path.dirname(
        os.path.abspath(
            os.path.join(__file__, '..')))

with open(os.path.join(ROOT_DIR, 'input_defaults.json')) as f:
    options = json.load(f)

options.update(pyiets.read.infile(options['input_file']))

os.rmdir(os.path.join(WORKDIR, options['mode_folder']))
os.rmdir(os.path.join(WORKDIR, options['output_folder']))
