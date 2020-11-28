# Create Paired File list with preprocessed files
import glob
import pandas as pd
import numpy as np
import os
import sys
import re

import matplotlib.pyplot as plt

import h5py

if __name__ == '__main__':

    case = "all"
    #case = "reduced"
    outfile_root = "../../data/preprocessed/TAASRAD19/"

    if case == "all":    
        df = pd.read_csv("../../data/preprocessed/TAASRAD19_list_precip.csv")
        file_list = df["date"].values
    if case == "reduced":
        df = pd.read_csv("../../data/preprocessed/TAASRAD19_list_precip_reduced.csv")
        file_list = df["date"].values
    else:
        print("unknown case !!")

    f=open('../../data/preprocessed/TAASRAD19_train_200_'+case+'.csv', 'w')
    print(",fname,fnext",file=f)
    count = 0
    
    for fname in file_list:
        infile = outfile_root + fname
        print(infile)
        tstr = re.search('_T..._',infile).group()
        tnum = int(tstr[2:5])
        tnext = '_T%03d_' % (tnum+12)
        infile_next = infile.replace(tstr,tnext)
        if os.path.exists(infile_next):
            h5fname = infile.split('/')[-1]
            h5fnext = infile_next.split('/')[-1]
            print("%d,%s,%s" % (count,h5fname,h5fnext),file=f)
            count = count + 1
