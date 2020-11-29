# Create Paired File list with preprocessed files
import glob
import os
import sys
import re
import subprocess

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from datetime import timedelta, datetime

import h5py

if __name__ == '__main__':

    #case = "all"
    case = "reduced"
    outfile_root = "../../data/preprocessed/DWD_RYDL/"

    if case == "all":    
        df = pd.read_csv("../../data/preprocessed/DWD_list_precip.csv")
        file_list = df["date"].values
    if case == "reduced":
        df = pd.read_csv("../../data/preprocessed/DWD_list_precip_reduced.csv")
        file_list = df["date"].values
    else:
        print("unknown case !!")

    f=open('../../data/preprocessed/DWD_RYDL_train_200_'+case+'.csv', 'w')
    print(",fname,fnext",file=f)
    count = 0
    
    local_path = "../../data/preprocessed/DWD_RYDL_" + case + "/"
    if not os.path.exists(local_path):
        os.mkdir(local_path)

    #### 200709152000_IJ10.h5
    
    for i,fname in enumerate(file_list):
        fname = str(fname)
        f00 = fname[0:10]+"00"
        I = df["i"][i]
        J = df["j"][i]
        str_ij = "_IJ%d%d" % (I,J)
        # next time (+1h)
        fmt = '%Y%m%d%H%M'
        time1 = datetime.strptime(f00,fmt)
        time2 = time1 + timedelta(hours=1)
        fnext = time2.strftime(fmt)
        infile = outfile_root + f00 + str_ij+ ".h5"
        infile_next = outfile_root + fnext + str_ij + ".h5"
        print(infile,infile_next)
        if os.path.exists(infile) and os.path.exists(infile_next):
            h5fname = infile.split('/')[-1]
            h5fnext = infile_next.split('/')[-1]
            print("%d,%s,%s" % (count,h5fname,h5fnext),file=f)
            # copy file to new directory
            subprocess.run("cp %s %s" % (infile,local_path+h5fname),shell=True)
            subprocess.run("cp %s %s" % (infile_next,local_path+h5fnext),shell=True)
            count = count + 1
