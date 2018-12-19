import sys

supported_qc_progs = {
    'turbomole'
}


def _missingInputErrorMessage(parameter, filename):
    """TODO: to be defined1. """
    print('Missing input \'{}\' in {}'.format(parameter, filename),
          file=sys.stderr)
    raise SystemExit


def _wrongInputErrorMessage(parameter, value, filename):
    """TODO: to be defined1. """
    print('Wrong input \'{}: {}\' in {}'.format(parameter, value, filename),
          file=sys.stderr)
    raise SystemExit


def _notsupportedInputMessage(parameter, filename):
    """TODO: to be defined1. """
    print('Input \'{}\' in {} is NOT supported!'.format(parameter, filename),
          file=sys.stderr)
    raise SystemExit


def check_options(options):
    """TODO: to be defined1. """
    if not options['sp_control']['qc_prog']:
        _missingInputErrorMessage('qc_prog', options['input_file'])
    if not options['sp_control']['params']:
        _missingInputErrorMessage('params', options['input_file'])
    if options['mp'] < 1:
        _wrongInputErrorMessage('mp', options['mp'], options['input_file'])
    if options['sp_control']['qc_prog'] not in supported_qc_progs:
        _notsupportedInputMessage('qc_prog',
                                  options['input_file'])
