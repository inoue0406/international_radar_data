import glob
import pandas as pd
import numpy as np
import os
import sys

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
        
        import pdb;pdb.set_trace()


