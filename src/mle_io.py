#! /usr/bin/env python3
import csv
from math import radians
import mle_core

DATASET_FILE = "../data/apogee-rc-DR14-back.csv"


'''
READ
'''
def read_dataset():
    data = mle_core.Data()
    f = open(DATASET_FILE, 'r')
    reader = csv.reader(f)
    for row in reader:
        data.l.append(radians(float(row[0])))
        data.b.append(radians(float(row[1])))
        data.vr.append(float(row[2]))
        data.r.append(float(row[3]))

    '''
    print(data.l[0])
    print(data.b[0])
    print(data.vr[0])
    print(data.r[0])
    '''
    print("Data is success readed, size = " + 
            str(len(data.l)))
    return data
