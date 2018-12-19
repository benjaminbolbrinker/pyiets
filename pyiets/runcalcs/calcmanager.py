import multiprocessing

import pyiets.runcalcs.turbomole as turbomole


def start_tm_single_points(folders, calc_options,
                           nthreads, restartfilename):
    with multiprocessing.Pool(processes=nthreads) as pool:
        manager = multiprocessing.Manager()
        lock = manager.Lock()
        params = [(restartfilename, lock, folder, calc_options)
                  for folder in folders]

        pool.starmap(turbomole.run, params)
#  [turbomole.run(*params[idx])
#   for idx, mode_folder in enumerate(folders)]

#  def restart_tm_single_points(outfolder, calc_options,
#                               nthreads, restartfilename):
#      if os.path.exists(restartfilename):
#          with open(restartfilename, 'r') as restartfile:
#              mode_folders = set([f.path for f in os.scandir(outfolder)
#                                  if f.is_dir()]) \
#                           - set(restartfile.read().split())
#
#      with multiprocessing.Pool(processes=nthreads) as pool:
#          manager = multiprocessing.Manager()
#          lock = manager.Lock()
#          params = [(restartfilename, lock, mode_folder, calc_options)
#                    for mode_folder in mode_folders]
#          pool.starmap(turbomole.run, params)
#          #  [turbomole.run(*params[idx])
#          #   for idx, mode_folder in enumerate(mode_folders)]
