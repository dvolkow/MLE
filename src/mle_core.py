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
    l  = []
    b  = []
    r  = []
    vr = []




'''
@distcos   = R^2 * cos^2(b) 
@dblcos    = 2 * r * cos(b) * cos(l)
@lsinbcos  = cos(b) * sin(l)
@beta[0]   = -cos(b) * cos(l)
@beta[1]   = -cos(b) * sin(l)
@beta[2]   = -sin(l)
'''
class Cache:
    distcos  = []
    dblcos   = []
    lsinbcos = []
    beta     = [[] for i in range(BETA_SIZE)]

    def __init__(self, Data):
        for i in range(len(Data.b)):
            self.distcos.append(Data.r[i] ** 2 * math.cos(Data.b[i]) ** 2)
            self.dblcos.append(2 * math.cos(Data.b[i]) * math.cos(Data.l[i]) *
                    Data.r[i])
            self.lsinbcos.append(math.sin(Data.l[i]) * math.cos(Data.b[i]))
            self.beta[0].append(- math.cos(Data.l[i]) * math.cos(Data.b[i])) 
            self.beta[1].append(- math.sin(Data.l[i]) * math.cos(Data.b[i])) 
            self.beta[2].append(- math.sin(Data.b[i])) 

    def r(self, r0, i):
        return math.sqrt(r0 ** 2 + self.distcos[i] - r0 * self.dblcos[i])




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
def v_sun(u, v, w, i):
    return -u * g_cache.beta[0][i] - v * g_cache.beta[1][i] - w * math.sin(data.b[i])

def vr_calc(R_0, A, i):
    return -2 * A * (g_cache.r(R_0, i) - R_0) * R_0 / (g_cache.r(R_0, i)) * math.sin(data.l[i]) * math.cos(data.b[i]) 



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
    R_0   = parameters[0]
    A     = parameters[1]
    u     = parameters[2]
    v     = parameters[3]
    w     = parameters[4]
    #sigma = parameters[5]
    #assert(sigma > 0)

    vr = [0 for i in range(len(data.l))]

    for i in range(len(data.l)):
        vr[i] = vr_calc(R_0, A, i) + v_sun(u, v, w, i)

    sigma = stdev(vr)

    L     = - len(data.l) * math.log(math.sqrt(2 * math.pi) * sigma)    
    for i in range(len(data.l)):
        L -=  (vr[i] - data.vr[i])**2 / (2 * sigma ** 2)
    
    print(R_0, A, sigma, u, v, w)
    return -L



def vr_optimize():
    model = minimize(likelyhood_log, MLE_START, method = 'CG')
    return model
