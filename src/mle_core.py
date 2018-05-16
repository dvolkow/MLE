#! /usr/bin/env python3
import math
import numpy  as np
import mle_io as io
from statistics     import stdev
from scipy.optimize import minimize

# -- configure
from mle_cfg import THETA_START_IDX
from mle_cfg import DEFAULT_PARAM_COUNT
# -- types:
from mle_types import Data
from mle_types import ModelParameters
from mle_types import Cache
# -- wrappers:
import mle_wrappers as wps



'''
Globals: 
    @data:    array with dataset, type Data
    @g_cache: used for fast get trigonomery
'''
data    = io.read_dataset()
g_cache = Cache(data)



def v_sun(u, v, w):
    return -u * g_cache.beta[0] - v * g_cache.beta[1] - w * np.sin(data.b)


def vr_calc(R_0, A, n = 1, theta = None):
    dR = g_cache.r(R_0, data) - R_0
    pr = R_0 / (g_cache.r(R_0, data)) * np.sin(data.l) * np.cos(data.b) # how name it?
    vr = -2 * A * dR * pr
    if n > 1:
        for i in range(THETA_START_IDX, n + 1):
            vr += dR ** (i) / math.factorial(i) * theta[i - THETA_START_IDX] * pr
    return vr



'''
Need for correct and more fast optimize. 
Discuss: optimized surface may is not smooth
'''
@wps.not_implemented
def grad_L():
    return []



@wps.likelyhood_basic
def likelyhood_log(parameters):
    n = len(parameters) - DEFAULT_PARAM_COUNT
    theta = None
    if (n < 2): 
        R_0, A, u, v, w   = parameters
    else:
        R_0 = parameters[0]
        A   = parameters[1]
        u   = parameters[2]
        v   = parameters[3]
        w   = parameters[4]
        theta = list(parameters[DEFAULT_PARAM_COUNT + 1:])
    vr = vr_calc(R_0, A, n = n, theta = theta) + v_sun(u, v, w)

    sigma = np.std(vr)

    L = - len(data.l) * math.log(math.sqrt(2 * math.pi) * sigma)    
    L -= np.sum(np.power(vr - data.vr, 2)) / (2 * sigma ** 2)
    
    return -L, sigma




'''
Return model obj
'''
@wps.optimize_out
def vr_optimize(function, start_values, optimize_type):
    def cb(arg):
        print("Current solution: {lf}\r".format(lf = str(arg)[1:-1].split()), end = '\r')
    return minimize(function, start_values, method = optimize_type, callback=cb)

