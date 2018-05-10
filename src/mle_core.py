#! /usr/bin/env python3
import math
import numpy as np
import mle_io as io
from statistics import stdev
from scipy.optimize import minimize


BETA_SIZE = 3
MLE_START = np.array([8, 16, 12, 24, 6])


'''
Warning about incomplete function
'''
def not_implemented(function):
    print("Need implementation for " + function.__name__)


'''
@l:  galactical longtitude
@b:  galactical latitude
@r:  distantion from Sun (kpc)
@vr: radial velocity (kmps)
'''
class Data:
    l  = np.array([])
    b  = np.array([])
    r  = np.array([])
    vr = np.array([])




'''
@distcos   = R^2 * cos^2(b) 
@dblcos    = 2 * r * cos(b) * cos(l)
@lsinbcos  = cos(b) * sin(l)
@beta[0]   = -cos(b) * cos(l)
@beta[1]   = -cos(b) * sin(l)
@beta[2]   = -sin(l)
'''
class Cache:
    distcos  = np.array([])
    dblcos   = np.array([])
    lsinbcos = np.array([])
    beta     = [np.array([]) for i in range(BETA_SIZE)]

    def __init__(self, data):
        self.distcos  = data.r * data.r * np.cos(data.b) * np.cos(data.b)
        self.dblcos   = np.array([2 for i in range(len(data.b))]) * data.r * np.cos(data.b) * np.cos(data.l) 
        self.lsinbcos = np.sin(data.l) * (np.cos(data.b))
        self.beta[0]  = - np.cos(data.l) * np.cos(data.b)
        self.beta[1]  = - np.sin(data.l) * np.cos(data.b) 
        self.beta[2]  = - np.sin(data.b) 

    def r(self, r0):
        return np.sqrt(np.array([r0 ** 2 for i in range(len(data.b))]) + 
                self.distcos - np.array([r0 for i in range(len(data.b))])* self.dblcos)




'''
Globals: 
    @data:    array with dataset, type Data
    @g_cache: used for fast get trigonomery
'''
data = io.read_dataset()
g_cache = Cache(data)




'''
TODO: create fabrique \ another generator 
      for such functions as vr
'''
def v_sun(u, v, w):
    return -u * g_cache.beta[0] - v * g_cache.beta[1] - w * np.sin(data.b)

def vr_calc(R_0, A):
    return -2 * A * (g_cache.r(R_0) - R_0) * R_0 / (g_cache.r(R_0)) * np.sin(data.l) * np.cos(data.b) 



'''
Need for correct and more fast optimize. 
Discuss: optimized surface may is not smooth
'''
@not_implemented
def grad_L():
    return []



'''
Only 1st degress of estimation polynom
TODO: extend to more freedoms
'''
def likelyhood_log(parameters):
    R_0, A, u, v, w   = parameters

    vr = vr_calc(R_0, A) + v_sun(u, v, w)

    sigma = np.std(vr)

    L = - len(data.l) * math.log(math.sqrt(2 * math.pi) * sigma)    
    L -= np.sum(np.power(vr - data.vr, 2)) / (2 * sigma ** 2)
    
    print(R_0, A, sigma, u, v, w)
    return -L


def vr_optimize():
    model = minimize(likelyhood_log, MLE_START, method = 'CG')
    return model
