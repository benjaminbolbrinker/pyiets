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

import sys

supported_qc_progs = {
    'turbomole',
    'gaussian'
}


def _missingInputErrorMessage(parameter, filename):
    '''Print error message

    Parameters
    ----------
        parameter : :obj:`str`
            parameter which is missing.
        filename : :obj:`str`
            filename where error occured.

    '''
    print('Missing input \'{}\' in {}'.format(parameter, filename),
          file=sys.stderr)
    raise SystemExit


def _wrongInputErrorMessage(parameter, value, filename):
    '''Print error message

    Parameters
    ----------
        parameter : :obj:`str`
            parameter which is missing.
        value :
            wrong value.
        filename : :obj:`str`
            filename where error occured.

    '''
    print('Wrong input \'{}: {}\' in {}'.format(parameter, value, filename),
          file=sys.stderr)
    raise SystemExit


def _notsupportedInputMessage(parameter, filename):
    '''Print error message

    Parameters
    ----------
        parameter : :obj:`str`
            parameter which is missing.
        filename : :obj:`str`
            filename where error occured.

    '''
    print('Input \'{}\' in {} is NOT supported!'.format(parameter, filename),
          file=sys.stderr)
    raise SystemExit


def check_options(options):
    '''Check for validity

    Parameters
    ----------
        options : :obj:`dict`
            contains the input options for pyiets.

    Raises
    ------
        SystemExit
            if invalt key value ist found in options

    '''
    if not options['sp_control']['qc_prog']:
        _missingInputErrorMessage('qc_prog', options['input_file'])
    if not options['sp_control']['params']:
        _missingInputErrorMessage('params', options['input_file'])
    if options['mp'] < 1:
        _wrongInputErrorMessage('mp', options['mp'], options['input_file'])
    if options['sp_control']['qc_prog'] not in supported_qc_progs:
        _notsupportedInputMessage('qc_prog',
                                  options['input_file'])
