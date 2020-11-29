import glob
import pandas as pd
import numpy as np
import os
import sys

import matplotlib.pyplot as plt

import h5py

if __name__ == '__main__':
    """
    Draw histogram of DWD RYDL data for data selection
    """
    df = pd.read_table("../../data/preprocessed/DWD_list_precip.csv",sep="\s+")
         
    df['rain_mean'].hist(bins=20)
    plt.savefig("../../result/DWD_RYDL/histogram/DWD_hist_rain_mean.png")
    plt.close()    
    df['rain_max'].hist(bins=20)
    plt.savefig("../../result/DWD_RYDL/histogram/DWD_hist_rain_max.png")
    plt.close()
    # log scale
    plt.hist(df['rain_mean'],bins=20,log=True)
    plt.savefig("../../result/DWD_RYDL/histogram/DWD_hist_rain_log_mean.png")
    plt.close()    
    plt.hist(df['rain_max'],bins=20,log=True)
    plt.savefig("../../result/DWD_RYDL/histogram/DWD_hist_rain_log_max.png")
    plt.close()

    print("size of the dataset",len(df))
    for th in [0.01,0.02,0.05,0.1,0.2,0.4,1.0]:
        print("number of samples over ",th,", ",sum(df["rain_mean"]>th))

    # save reduced sample data
    df_reduced = df[df["rain_mean"]>0.05]
    df_reduced.to_csv("../../data/preprocessed/DWD_list_precip_reduced.csv",
                      index=False)

    import pdb;pdb.set_trace()
    
