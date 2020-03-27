from .helpers import root
from .beluga import bvp_algorithm, guess_generator, ocp2bvp, run_continuation_set, solve, add_logger, bvpsol
from .continuation import ContinuationList as init_continuation
from .problem import OCP
from .scaling import Scaling
from functools import partial
import os
import glob

import logging
logging.BELUGA = logging.INFO - 5
logging.addLevelName(logging.BELUGA, 'BELUGA')
logging.beluga = partial(logging.log, logging.BELUGA)

from beluga.release import __version__, __splash__

modules = glob.glob(os.path.dirname(__file__)+"/*.py")
__all__ = [os.path.basename(f)[:-3] for f in modules]

import numpy
DTYPE = numpy.float64
