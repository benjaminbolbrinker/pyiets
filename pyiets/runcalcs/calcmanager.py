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
import pyiets.runcalcs.gaussian as gaussian
import pyiets.runcalcs.artaios as artaios
import pyiets.runcalcs.tm2unformcl as tm2unformcl
import pyiets.runcalcs.tm2unformsoc as tm2unformsoc
import pyiets.runcalcs.g092unform as g092unform


def start_tm_single_points(folders, options, restarfileloc=None):
    '''Start turbomole calculations asynchronously in specified folders.

    Parameters
    ----------
    folders : :obj:`list`
        containing foldernames (str)
    coord : :obj:`str`
        name of turbomole coord file (has to be present in each folder).
    params : :obj:`dict`
        ASE params for turbomole.
    nthreads : int
        number of threads.
    restartfilename : :obj:`str`, optional
        name of restartfile.
    '''
    with multiprocessing.Pool(processes=options['mp']) as pool:
        manager = multiprocessing.Manager()
        lock = manager.Lock()
        params = [(folder, options, restarfileloc, lock)
                  for folder in folders]
        pool.map(turbomole.run, params)
        pool.close()
        pool.join()


def start_gaussian_single_points(folders, options, restarfileloc=None):
    '''Start turbomole calculations asynchronously in specified folders.

    Parameters
    ----------
    folders : :obj:`list`
        containing foldernames (str)
    coord : :obj:`str`
        name of turbomole coord file (has to be present in each folder).
    params : :obj:`dict`
        ASE params for turbomole.
    nthreads : int
        number of threads.
    restartfilename : :obj:`str`, optional
        name of restartfile.
    '''
    with multiprocessing.Pool(processes=options['mp']) as pool:
        manager = multiprocessing.Manager()
        lock = manager.Lock()
        params = [(folder, options, restarfileloc, lock)
                  for folder in folders]
        pool.map(gaussian.run, params)
        pool.close()
        pool.join()


def start_artaios(folders, options, restarfileloc=None):
    '''Start artaios calculations asynchronously in specified folders.

    Parameters
    ----------
    folders : :obj:`list`
        containing foldernames (str)
    coord : :obj:`str`
        name of turbomole coord file (has to be present in each folder).
    params : :obj:`dict`
        ASE params for turbomole.
    nthreads : int
        number of threads.
    restartfilename : :obj:`str`, optional
        name of restartfile.
    '''

    with multiprocessing.Pool(processes=options['mp']) as pool:
        manager = multiprocessing.Manager()
        lock = manager.Lock()
        params = [(folder, options, restarfileloc, lock)
                  for folder in folders]
        pool.imap(artaios.run, params)
        pool.close()
        pool.join()


def start_g092unform(folders, options, restarfileloc=None):
    '''Start artaios calculations asynchronously in specified folders.

    Parameters
    ----------
    folders : :obj:`list`
        containing foldernames (str)
    coord : :obj:`str`
        name of turbomole coord file (has to be present in each folder).
    params : :obj:`dict`
        ASE params for turbomole.
    nthreads : int
        number of threads.
    restartfilename : :obj:`str`, optional
        name of restartfile.
    '''

    with multiprocessing.Pool(processes=options['mp']) as pool:
        params = [(folder, options)
                  for folder in folders]
        pool.imap(g092unform.run, params)
        pool.close()
        pool.join()


def start_tm2unformcl(folders, options, restarfileloc=None):
    '''Start artaios calculations asynchronously in specified folders.

    Parameters
    ----------
    folders : :obj:`list`
        containing foldernames (str)
    coord : :obj:`str`
        name of turbomole coord file (has to be present in each folder).
    params : :obj:`dict`
        ASE params for turbomole.
    nthreads : int
        number of threads.
    restartfilename : :obj:`str`, optional
        name of restartfile.
    '''

    with multiprocessing.Pool(processes=options['mp']) as pool:
        params = [(folder, options)
                  for folder in folders]
        pool.imap(tm2unformcl.run, params)
        pool.close()
        pool.join()


def start_tm2unformsoc(folders, options, restarfileloc=None):
    '''Start artaios calculations asynchronously in specified folders.

    Parameters
    ----------
    folders : :obj:`list`
        containing foldernames (str)
    coord : :obj:`str`
        name of turbomole coord file (has to be present in each folder).
    params : :obj:`dict`
        ASE params for turbomole.
    nthreads : int
        number of threads.
    restartfilename : :obj:`str`, optional
        name of restartfile.
    '''

    with multiprocessing.Pool(processes=options['mp']) as pool:
        params = [(folder, options)
                  for folder in folders]
        pool.imap(tm2unformsoc.run, params)
        pool.close()
        pool.join()
