#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import snfio

if __name__ == '__main__':
    parser = snfio.snfParser('snf.out')
    #  print(parser._get_natoms())
    #  parser.get_molecule().print()
    #  print(parser.get_nmodes())
    parser.get_mode(1).print()
