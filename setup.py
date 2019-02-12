#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# PyIETS

# Postprocessing tool for calculating the IETS intensity and hence the
# electron-phonon-interaction
#
# Copyright (C) 2019 Benjamin Bolbrinker, Michael Deffner,
#                    Martin Zoellner, Carmen Herrmann
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from disutils.core import setup

setup(name='pyiets',
      version='0.0.1',
      description='Post processing tool for SNF (MoViPac)',
      author='Benjamin Bolbrinker',
      author_email='benjamin.bolbrinker@chemie.uni-hamburg.de',
      license='GPLv3',
      url='',
      packages=[],
      scripts=['pyiets.py'],
      zip_safe=False)
