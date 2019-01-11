import os
import pyiets.io.snfio


class Preprocessor():
    def __init__(self, workdir, options):
        self.workdir = workdir
        self.options = options
        self.snf_parser = pyiets.io.snfio.SnfParser(
            os.path.join(self.workdir, self.options['snf_out'])
        )
