#! /usr/bin/env python3
import csv
import numpy as np
from math import radians
import mle_core

DATASET_FILE = "../data/apogee-rc-DR14-full.csv"


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
