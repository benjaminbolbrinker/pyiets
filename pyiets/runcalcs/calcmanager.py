# PyIETS

# Postprocessing tool for calculating the IETS intensity and hence the
# electron-phonon-interaction
#
# Copyright (C) 2019 Benjamin Bolbrinker, Michael Deffner, Carmen Herrmann
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

import multiprocessing

import pyiets.runcalcs.turbomole as turbomole
import pyiets.runcalcs.artaios as artaios
import pyiets.runcalcs.tm2unformcl as tm2unformcl


def start_tm_single_points(folders, coord, params,
                           nthreads, restartfilename):
    '''Start turbomole calculations asynchronously in specified folders.

    Args:
        folders (list): containing foldernames (str)
        coord (str): name of turbomole coord file (has to be present in each
                     folder).
        params (dict): ASE params for turbomole.
        nthreads (int): number of threads.
        restartfilename (str): name of restartfile.
    '''
    with multiprocessing.Pool(processes=nthreads) as pool:
        manager = multiprocessing.Manager()
        lock = manager.Lock()
        params = [(coord, restartfilename, lock, folder, params)
                  for folder in folders]
        pool.map(turbomole.run, params)


def start_artaios(folders, options):
    '''Start turbomole calculations asynchronously in specified folders.

    Args:
        folders (list): containing foldernames (str)
        coord (str): name of turbomole coord file (has to be present in each
                     folder).
        params (dict): ASE params for turbomole.
        nthreads (int): number of threads.
        restartfilename (str): name of restartfile.
    '''

    with multiprocessing.Pool(processes=options['mp']) as pool:
        manager = multiprocessing.Manager()
        lock = manager.Lock()
        params = [(folder, options)
                  for folder in folders]
        pool.imap(tm2unformcl.run, params)
        pool.close()
        pool.join()

    with multiprocessing.Pool(processes=options['mp']) as pool:
        manager = multiprocessing.Manager()
        lock = manager.Lock()
        params = [(folder, options, lock)
                  for folder in folders]
        pool.imap(artaios.run, params)
        pool.close()
        pool.join()
