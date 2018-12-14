#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pyiets.io.snfio
import pyiets.io.createInput
import pyiets.io.parseInput

if __name__ == '__main__':
    parser = pyiets.io.snfio.SnfParser('snf.out')
    print(parser._get_natoms())
    parser.get_molecule().print()
    print(parser.nmodes)
    parser.get_mode(1).print()
    pyiets.io.snfio.exportMolecule('snf.out', 'xyz')
    pyiets.io.createInput.writeDisortion('turbomole', 'snf.out', delta=0.1)

    inparser = pyiets.io.parseInput.InputParser('input.json')
