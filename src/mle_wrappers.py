#! /usr/bin/env python3
from mle_types import ModelParameters
from mle_cfg import DEFAULT_PARAM_COUNT
from mle_cfg import THETA_START_IDX

g_mle_sigma = 0

'''
Warning about incomplete function
'''
def not_implemented(function):
    print("Need implementation for " + function.__name__)


'''
Output to stdout parameters that was finded
here, @mparameters is ModelParameters type
'''
def mle_print_solution(mparameters):
    print("sigma: ", mparameters.sigma)
    print("R_0:   ", mparameters.R_0)
    print("A:     ", mparameters.A)
    print("u:     ", mparameters.u)
    print("v:     ", mparameters.v)
    print("w:     ", mparameters.w)
    for i in range(len(mparameters.theta)):
        print("theta{i}: ".format(i = THETA_START_IDX + i), mparameters.theta[i])

def mle_solution_show(mparameters):
    print("--------MLE_SOLUTION:--------")
    mle_print_solution(mparameters)

def lse_solution_show(mparameters):
    print("--------LSE_SOLUTION:--------")
    mle_print_solution(mparameters)

'''
Otput parameters 
'''
def optimize_out(function):
    global g_mle_sigma
    def optimize_out_dbg(f, start_values, optimize_type):
        model = function(f, start_values, optimize_type)
        print("\nSolution get with {status} status and stopped.".format(status = model["success"]))
        print("Jacobian: {jacoby}".format(jacoby = model["jac"]))
        mp     = ModelParameters()

        mp.lf  = model["fun"]
        mp.R_0 = model["x"][0]
        mp.A   = model["x"][1]
        mp.u   = model["x"][2]
        mp.v   = model["x"][3]
        mp.w   = model["x"][4]
        mp.sigma = g_mle_sigma
        for i in range(len(model["x"][DEFAULT_PARAM_COUNT + 1:])):
            mp.theta.append(model["x"][DEFAULT_PARAM_COUNT + 1 + i])

        #mle_print_solution(mp)
        return mp
    return optimize_out_dbg



def likelyhood_out(likelyhood_f):
    def likelyhood_log_dbg(parameters):
        L, sigma = likelyhood_f(parameters)
        print("Current -L: {lf}, sigma: {sigma}\r".format(lf = L, sigma = sigma), end = '')
        return L
    return likelyhood_log_dbg


def likelyhood_basic(likelyhood_f):
    def likelyhood_log_L(parameters):
        L, sigma = likelyhood_f(parameters)
        return L
    return likelyhood_log_L


