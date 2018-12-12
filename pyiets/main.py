#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import snfio
import createInput

if __name__ == '__main__':
    parser = snfio.SnfParser('snf.out')
    print(parser._get_natoms())
    parser.get_molecule().print()
    print(parser.nmodes)
    parser.get_mode(1).print()
    snfio.exportMolecule('snf.out', 'xyz')
    createInput.writeDisortion(0, 'xyz')
