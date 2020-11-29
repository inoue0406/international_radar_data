import glob
import pandas as pd
import numpy as np
import os
import sys

import matplotlib.pyplot as plt

import h5py

def rainfall_to_dBZ(rainfall_intensity, a=None, b=None):
    """Convert the rainfall intensity to dBZ
    Parameters
    ----------
    rainfall_intensity : np.ndarray
    a : float32, optional
    b : float32, optional
    Returns
    -------
    pixel_vals : np.ndarray
    """
    if a is None:
        a = 58.53
    if b is None:
        b = 1.56
    dBR = np.log10(rainfall_intensity) * 10.0
    dBZ = dBR * b + 10.0 * np.log10(a)
    #pixel_vals = (dBZ + 10.0) / 70.0
    return dBZ

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
    """
    Draw histogram of TAASRAD19 data for data selection
    """
    
    df = pd.read_csv("../../data/preprocessed/TAASRAD19_list_precip.csv")

    # remove "all_data" entry
    rem = ~df["date"].str.contains('all_data')
    df_rem = df.loc[rem]
    
    # convert dBZ to rainfall
    df_rem.columns = ['date', 'i', 'j', 'dBZ_mean', 'dBZ_max','rain_mm_mean', 'rain_mm_max']
    #df_rem["rain_mm_mean"]=dBZ_to_rainfall(df_rem['dBZ_mean'])
    #df_rem["rain_mm_max"]=dBZ_to_rainfall(df_rem['dBZ_max'])
     
    df_rem['rain_mm_mean'].hist(bins=20)
    plt.savefig("../../result/TAASRAD19/histogram/TAASRAD19_hist_rain_mean.png")
    plt.close()    
    df_rem['rain_mm_max'].hist(bins=20)
    plt.savefig("../../result/TAASRAD19/histogram/TAASRAD19_hist_rain_max.png")
    plt.close()
    df_rem['dBZ_mean'].hist(bins=20)
    plt.savefig("../../result/TAASRAD19/histogram/TAASRAD19_hist_reflectivity_mean.png")
    plt.close()    
    df_rem['dBZ_max'].hist(bins=20)
    plt.savefig("../../result/TAASRAD19/histogram/TAASRAD19_hist_reflectivity_max.png")
    plt.close()

    # log scale
    plt.hist(df_rem['rain_mm_mean'],bins=20,log=True)
    plt.savefig("../../result/TAASRAD19/histogram/TAASRAD19_hist_rain_mean_log.png")
    plt.close()    
    plt.hist(df_rem['rain_mm_max'],bins=20,log=True)
    plt.savefig("../../result/TAASRAD19/histogram/TAASRAD19_hist_rain_max_log.png")
    plt.close()

    for th in [0.01,0.02,0.04,0.1,0.2,0.4,1.0]:
        print("number of samples over ",th,", ",sum(df_rem["rain_mm_mean"]>th))

    # save reduced sample data
    df_reduced = df_rem[df_rem["rain_mm_mean"]>0.1]
    df_reduced.to_csv("../../data/preprocessed/TAASRAD19_list_precip_reduced.csv",
                      index=False)

    import pdb;pdb.set_trace()
