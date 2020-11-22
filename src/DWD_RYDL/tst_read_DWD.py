import glob
import pandas as pd
import numpy as np
import os
import sys
import re

import matplotlib.pyplot as plt

import h5py

if __name__ == '__main__':
    input_file = "../../data/DWD_RYDL/RYDL.hdf5"
    print(input_file)
    h5file = h5py.File(input_file,'r')
    date_list =list(h5file.keys())
    
    for date in date_list:
        if re.search(r'00$',date):
            R0 = h5file[date][()]
            print("Processing Date:",date,np.mean(R0),np.max(R0))
            plt.imshow(R0[:,:].astype(np.float32),vmin=0,vmax=5,origin='lower')
            plt.savefig('../../result/DWD_RYDL/tstout/rain_figure_'+date+'.png')
        else:
            print("skipped",date)
        import pdb;pdb.set_trace()

        

        



