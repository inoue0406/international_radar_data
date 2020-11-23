import glob
import pandas as pd
import numpy as np
import os
import sys
import re

import matplotlib.pyplot as plt

import h5py

def grid_write_h5(Rhour,date,outfile_root,fcsv):
    # from 900x900 data, generate a set of indexed grid
    imax = 4
    jmax = 4
    dx = 200
    
    for i in range(imax):
        for j in range(jmax):
            ii = 50 + i*dx
            jj = 50 + j*dx
            print("ii,jj",ii,jj)
            Rtmp = Rhour[:,ii:ii+dx,jj:jj+dx]
            # write to h5 file
            str_post = "_IJ%d%d" % (i,j)
            h5fname = date + str_post + ".h5"
            print('writing h5 file:',h5fname)
            h5file = h5py.File(outfile_root+h5fname,'w')
            h5file.create_dataset('R',data= Rtmp)
            print(date_m,i,j,np.mean(Rtmp),np.max(Rtmp),file=fcsv)
    #import pdb;pdb.set_trace()

if __name__ == '__main__':
    input_file = "../../data/DWD_RYDL/RYDL.hdf5"
    outfile_root = "../../data/preprocessed/DWD_RYDL/"
    print(input_file)
    h5file = h5py.File(input_file,'r')
    date_list =list(h5file.keys())
    
    fcsv = open("../../data/preprocessed/DWD_list_precip.csv","w")
<<<<<<< HEAD
    print("date,i,j,rain_mean,rain_max\n",file=fcsv)
=======
    print("date,date_nexrad,time_diff_sec,rain_mean,rain_max\n",file=fcsv)
>>>>>>> c4950c40cda603e936a24509e9f3f1def54de0c8

    for date in date_list:
        if re.search(r'00$',date):
            # loop throgh 00 05 10 ... 55min
            Rhour_list = []
            for t in range(12):
                min = t * 5
                date_m = re.sub("00$","%02d" % min,date)
                if date_m in date_list:
                    R0 = h5file[date_m][()]
                    print("Processing Date:",date_m,np.mean(R0),np.max(R0))
                    Rhour_list.append(R0)
                else:
                    print("date ",date_m," NOT FOUND in h5 file skipping")
                    continue
            if len(Rhour_list) == 12:
                Rhour = np.stack(Rhour_list) # time x H x W dimension
                # write to h5 file
                grid_write_h5(Rhour,date,outfile_root,fcsv)
            else:
                # if any of 12 sequence is mising, then skip
                print("skipped")
                continue
        else:
            print("skipped",date)


        

        



