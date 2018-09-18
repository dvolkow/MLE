#! /usr/bin/env python3
import numpy as np
import mle_core as core
import mle_io as io
from mle_wrappers import mle_solution_show
from mle_wrappers import lse_solution_show

from mle_cfg import MLE_START



if __name__ == '__main__':
    refdata = io.read_reference(2)
    data = core.vr_optimize(core.likelyhood_log, MLE_START, 'CG')
    mle_solution_show(data)
    lse_solution_show(refdata)


