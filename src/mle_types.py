#! /usr/bin/env python3
import numpy as np
from mle_cfg import BETA_SIZE
from mle_cfg import MLE_START

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


class ModelParameters:
    def __init__(self):
        self.R_0 = 0
        self.A   = 0
        self.v   = 0
        self.u   = 0
        self.w   = 0
        self.theta = []
        self.sigma = 0
        self.lf  = 0


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
        self.dblcos   = np.repeat(2, len(data.b)) * data.r * np.cos(data.b) * np.cos(data.l) 
        self.lsinbcos = np.sin(data.l) * (np.cos(data.b))
        self.beta[0]  = - np.cos(data.l) * np.cos(data.b)
        self.beta[1]  = - np.sin(data.l) * np.cos(data.b) 
        self.beta[2]  = - np.sin(data.b) 

    def r(self, r0, data):
        return np.sqrt(np.array([r0 ** 2 for i in range(len(data.b))]) + 
                self.distcos - np.repeat(r0, len(data.b)) * self.dblcos)



