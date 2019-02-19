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

import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyiets',
    version='0.0.1',
    author=('Benjamin Bolbrinker, Michael Deffner, ' +
            'Martin Zoellner, Carmen Herrmann'),
    author_email='benjamin.bolbrinker@chemie.uni.hamburg.de',
    description='A tool for calculating inelastic tunneling spectra',
    packages=['pyiets'],
    scripts=['bin/pyiets'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GPLv3',
        'Operating System :: Ubuntu 18.04'
    ],
    install_requires=[
        'ase',
        'numpy',
        'mendeleev',
        'cclib',
        'sphinx',
        'sphinxcontrib-bibtex',
        'numpydoc',
        'sphinx-rtd-theme',
    ],
)
