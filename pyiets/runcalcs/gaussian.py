import io
import os
import glob
import ase.io
# from ase.calculators.gaussian import Gaussian
from contextlib import redirect_stdout


def create_g09_input(g09_options, ase_molecule, filename):
    options = {
            'method': 'BP86',
            'basis': 'Def2SVP',
            'charge': 0,
            'multiplicity': 1,
            'nprocshared': 1,
            'grid': None,
            'force': False,
            'nosymmetry': True
            }

    options.update(g09_options)

    with open(filename, 'w') as fp:
        fp.write('%chk=g09.chk\n')
        fp.write('%NProcShared=' + str(options['nprocshared']) + '\n')
        fp.write('#P ' + options['method']
                       + '/' + options['basis']
                       + ' GFPrint')
        if options['nosymmetry']:
            fp.write(' NoSymmetry')
        if options['grid']:
            fp.write(' int=grid=' + options['grid'])
        if options['force']:
            fp.write(' force')
        fp.write('\n\n')
        fp.write('Title '
                 + ase_molecule.get_chemical_formula(mode='hill')
                 + '\n\n')
        fp.write(str(options['charge']) + ' '*4 +
                 str(options['multiplicity']) + '\n')
        for idx, vec in enumerate(ase_molecule.get_positions()):
            fp.write(ase_molecule.get_chemical_symbols()[idx] + ' '*4)
            for coord in vec:
                fp.write('{:.16f}'.format(coord) + ' '*4)
            fp.write('\n')
        fp.write('\n\n')
        fp.write('--Link1--\n')
        fp.write('%chk=g09.chk\n')
        fp.write('%NProcShared=' + str(options['nprocshared']) + '\n')
        fp.write('#P ' + options['method']
                       + '/' + options['basis']
                       + ' guess=read\n')
        fp.write('#P GFINPUT IOP(6/7=3)')
        if options['nosymmetry']:
            fp.write(' NoSymmetry')
        if options['grid']:
            fp.write(' int=grid=' + options['grid'])
        if options['force']:
            fp.write(' force')
        fp.write('\n')
        fp.write('# iop(5/33=3)\n')
        fp.write('# iop(3/33=1)\n\n')
        fp.write('Title '
                 + ase_molecule.get_chemical_formula(mode='hill')
                 + '\n\n')
        fp.write(str(options['charge']) + ' '*4 +
                 str(options['multiplicity']) + '\n')
        for idx, vec in enumerate(ase_molecule.get_positions()):
            fp.write(ase_molecule.get_chemical_symbols()[idx] + ' '*4)
            for coord in vec:
                fp.write('{:.16f}'.format(coord) + ' '*4)
            fp.write('\n')
        fp.write('\n\n')
        return


def run(params):
    """Run Turbomole calculation in specified folder.
    Removes all files before starting calculation.
    If successful safly write foldername in file. (Therefore
    lock has to be provided)

    Parameters
    ----------
        params : :obj:`list`
            folder : obj`str`
                name of folder to perform calculation in.
            options : :obj`dict`
                Options.
            restartfilename : :obj:`str`
                path to restartfile.
            lock : :obj:`multiprocessing.Manager.lock`
                lock for multiprocessing.
    """
    folder = params[0]
    options = params[1]
    restartfileloc = params[2]
    lock = params[3]

    cwd = os.getcwd()
    os.chdir(folder)

    infilename = 'g09.com'
    coord = options['dissotionoutname']
    lock.acquire()
    create_g09_input(g09_options=options['sp_control']['params'],
                     ase_molecule=ase.io.read(options['dissotionoutname']),
                     filename=infilename)
    lock.release()

    # Clean directory
    if options['restart']:
        files = glob.glob('*')
        cleanupFiles = files
        cleanupFiles.remove(coord)
        cleanupFiles.remove(infilename)
        for cleanupFile in cleanupFiles:
            os.remove(cleanupFile)

    # Run and redirect output
    g09outname = 'g09.log'
    if options['verbose']:
        print('''
Starting gaussian in \'{}\'
Redirecting output to \'{}\'
'''.format(folder, g09outname))
    f = io.StringIO()
    with open(g09outname, 'w') as f:
        with redirect_stdout(f):
            # subprocess.call(['g09', ' < ', infilename, ' > ', g09outname])
            os.system('g09 < ' + infilename + ' > ' + g09outname)

    os.chdir(cwd)

    if restartfileloc is not None:
        restartfile = os.path.join(restartfileloc,
                                   options['sp_restart_file'])
        lock.acquire()
        with open(restartfile, 'a') as restart_file:
            restart_file.write(folder + ' ')
        lock.release()
    # else:
        # restartfile = options['sp_restart_file']

    # Safefly write to restartfile
    return folder
