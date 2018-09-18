#! /usr/bin/env python3
import csv
import numpy as np
from math import radians
import mle_core

DATASET_FILE = "../data/apogee-rc-DR14-full.csv"
REFERENCE_FILE = "../result/ref.lse"


'''
READ
'''
def read_dataset():
    data = mle_core.Data()
    f = open(DATASET_FILE, 'r')
    reader = csv.reader(f)
    l, b, vr, r = ([], [], [], [])
    for row in reader:
        l.append(radians(float(row[0])))
        b.append(radians(float(row[1])))
        vr.append(float(row[2]))
        r.append(float(row[3]))

    data.l = np.array(l)
    data.b = np.array(b)
    data.vr = np.array(vr)
    data.r = np.array(r)
    print("Data is success readed, size = " + 
            str(len(data.l)))
    return data

'''
reference LSE result 
'''
def read_reference(n):
    refdata = mle_core.ModelParameters()
    with open(REFERENCE_FILE, 'r') as f:
        tg = f.readlines()[n - 1].split()
        refdata.R_0 = float(tg[1])
        refdata.sigma = float(tg[4])
        refdata.u = float(tg[5])
        refdata.v = float(tg[6])
        refdata.w = float(tg[7])
        refdata.A = float(tg[8])
        for i in range(len(tg[9:])):
            refdata.theta.append(float(tg[9 + i]))
    return refdata
