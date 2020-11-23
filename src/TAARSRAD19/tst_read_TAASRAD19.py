import glob
import pandas as pd
import numpy as np
import os
import sys

import matplotlib.pyplot as plt

import h5py

if __name__ == '__main__':
    root_dir = "../../data/TAASRAD19/hdf_archives/"
    file_list = sorted(glob.iglob(root_dir + '/*.hdf5'))
    
    for infile in file_list:
        print(infile)
        h5file = h5py.File(infile,'r')
        print("Variables Contained:",h5file.keys())
        R0 = h5file['0'][()]
        R1 = h5file['1'][()]
        h5file.close()
        
        for t in range(R0.shape[0]):
            tstr = "%03d" % t
            plt.imshow(R0[t,:,:].astype(np.float32),vmin=0,vmax=50,origin='lower')
            plt.savefig('../../result/TAASRAD19/tstout/R0_figure_'+tstr+'.png')
        for t in range(R1.shape[0]):
            tstr = "%03d" % t
            plt.imshow(R1[t,:,:].astype(np.float32),vmin=0,vmax=50,origin='lower')
            plt.savefig('../../result/TAASRAD19/tstout/R1_figure_'+tstr+'.png')

        

        

        



