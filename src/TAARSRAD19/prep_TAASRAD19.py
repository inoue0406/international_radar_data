import glob
import pandas as pd
import numpy as np
import os
import sys

import matplotlib.pyplot as plt

import h5py

if __name__ == '__main__':
    root_dir = "../../data/TAASRAD19/hdf_archives/"
    outfile_root = "../../data/preprocessed/TAASRAD19/"
    file_list = sorted(glob.iglob(root_dir + '/*.hdf5'))
    
    for infile in file_list:
        print(infile)
        h5file = h5py.File(infile,'r')
        print("Variables Contained:",h5file.keys())
        #import pdb;pdb.set_trace()
        R0 = h5file['0'][()]
        #R1 = h5file['1'][()]
        h5file.close()

        # Concatenate along time axis
        #Rall = np.concatenate([R0,R1])
        Rall = np.concatenate([R0])
        tsize = Rall.shape[0]
        dt = 12 # set 12step (1h) as one block
        dx = 200

        for t in range(0,tsize-dt,dt):
            for i in [0,1]:
                for j in [0,1]:
                    ii = 100 + i*100
                    jj = 100 + j*100
                    print("t,ii,jj",t,ii,jj)
                    Rtmp = Rall[t:t+dt,ii:ii+dx,jj:jj+dx]
                    # write to h5 file
                    h5fname = infile.split('/')[-1]
                    str_post = "_T%03d_IJ%d%d" % (t,i,j)
                    h5fname = h5fname.replace('.hdf5',str_post+'.h5')
                    print('writing h5 file:',h5fname)
                    h5file = h5py.File(outfile_root+h5fname,'w')
                    h5file.create_dataset('R',data= Rtmp)



        
