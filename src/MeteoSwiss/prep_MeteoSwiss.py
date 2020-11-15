#---------------------------------------------------
# Preprocess MeteoSwiss Data
#---------------------------------------------------
import glob
import subprocess
import sys
import os.path

import netCDF4
import numpy as np
import h5py
import pandas as pd

#def convert_int_rainfall():

if __name__ == '__main__':

    outfile_root = "../../data/preprocessed/MeteoSwiss/"
    
    # scale data
    fscale = pd.read_csv("../../data/MeteoSwiss/scale_rzc.txt",header=None)
    fscale = fscale[0].values[:]

    fname = "../../data/MeteoSwiss/samples-2018-128x128.nc"
    nc = netCDF4.Dataset(fname, 'r')

    for nt in range(180000):
        # scale to float data
        Rint = nc.variables['sequences'][nt,:,:,:,:]
        R = fscale[Rint][:,:,:,0].astype(np.float16)
        h5fname ="MeteoSwiss_samples_2018_128_%06d.h5" % nt
        print('writing h5 file:',h5fname)
        h5file = h5py.File(outfile_root+h5fname,'w')
        h5file.create_dataset('R',data= R)
