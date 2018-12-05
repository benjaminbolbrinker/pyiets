#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import snfio

if __name__ == '__main__':
    parser = snfio.snfParser('snf.out')
    #  print(parser._get_natoms())
    #  print(parser.get_molecule())
    #  print(parser.get_nmodes())
    print(parser.get_mode(1))
