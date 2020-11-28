import glob
import pandas as pd
import numpy as np
import os
import sys

import matplotlib.pyplot as plt

import h5py

def dBZ_to_rainfall(dBZ, a=None, b=None):
    """Convert dBZ to rainfall intensity
    Parameters
    ----------
    dBZ : np.ndarray
    a : float32, optional
    b : float32, optional
    Returns
    -------
    rainfall : np.ndarray
    """
    if a is None:
        a = 58.53
    if b is None:
        b = 1.56
    dBR = (dBZ - 10.0 * np.log10(a))/b
    rainfall = 10 ** (dBR/10.0)
    return rainfall

if __name__ == '__main__':
    root_dir = "../../data/TAASRAD19/hdf_archives/"
    outfile_root = "../../data/preprocessed/TAASRAD19/"
    file_list = sorted(glob.iglob(root_dir + '/*.hdf5'))

    fcsv = open("../../data/preprocessed/TAASRAD19_list_precip.csv","w")
    print("date,i,j,rain_mean,rain_max",file=fcsv)
    
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
                    # rainfal intensity
                    rain_tmp = dBZ_to_rainfall(Rtmp)
                    # convert to masked array
                    #flg = (Rtmp==0)*1
                    #Rtmp_ma = np.ma.masked_array(Rtmp,mask=flg,fill_value=0.0)
                    # write to h5 file
                    h5fname = infile.split('/')[-1] 
                    str_post = "_T%03d_IJ%d%d" % (t,i,j)
                    h5fname = h5fname.replace('.hdf5',str_post+'.h5')
                    print('writing h5 file:',h5fname)
                    h5file = h5py.File(outfile_root+h5fname,'w')
                    h5file.create_dataset('R',data= rain_tmp)
                    # write info to file
                    print("%s,%d,%d,%f,%f" % (h5fname,i,j,
                                              Rtmp.mean(),Rtmp.max(),
                                              rain_tmp.mean(),rain_tmp.max()),
                          file=fcsv,flush=True)
        
