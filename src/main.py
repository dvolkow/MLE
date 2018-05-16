#! /usr/bin/env python3
import numpy as np
import mle_core as core
import mle_io as io

from mle_cfg import MLE_START


if __name__ == '__main__':
    core.vr_optimize(core.likelyhood_log, MLE_START, 'CG')
