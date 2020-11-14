# scripts for downloading NEXRAD raw data

import glob
import pandas as pd
import numpy as np
import os
import subprocess
import sys

if __name__ == '__main__':
    # read case name from command line
    argvs = sys.argv
    argc = len(argvs)

    if argc != 4:
        print('Usage: python download_aws_nexrad.py setting site start_date')
        quit()

    setting = argvs[1]
    isite = int(argvs[2]) # site 0-155
    start_date = argvs[3]
    print("setting:",setting)
    print("site:",isite)
    print("date:",start_date)

    site_list=pd.read_csv("../data/NEXRAD_site_list.csv",header=None)
    site_list=site_list[0].tolist()

    setting = "train"
    #setting = "valid"
    #site = "KTLX"
    site = site_list[isite]
    
    if setting == "train":
        # select 2015 and 2016 for training
        #dates = pd.date_range(start='2015-01-01 00:00', end='2016-12-31 22:00', freq='H')
        #dates = pd.date_range(start='2015-04-01 00:00', end='2016-12-31 22:00', freq='H')
        dates = pd.date_range(start=start_date+' 00:00', end='2016-12-31 22:00', freq='H')
    elif setting == "valid":
        # select 2017 for validation
        dates = pd.date_range(start='2017-01-01 00:00', end='2017-12-31 22:00', freq='H')
        
    # file format "2p-jmaradar5_2015-01-01_0000utc.h5"
    
    # We choose loop through continuous times for missed-file checking and 
    # checking for valid X-Y pairs
    
    for n,date in enumerate(dates):
        print(date)
        # set paths
        s3_path = date.strftime("s3://noaa-nexrad-level2/%Y/%m/%d/")
        s3_path = s3_path + site + "/"
        print(s3_path)
        local_path = "../data/NEXRAD_original/"+site
        if not os.path.exists(local_path):
            os.mkdir(local_path)
        # copy
        command = "aws s3 cp " + s3_path + " "+ local_path+"/" + " --recursive --no-sign-request"
        subprocess.run(command,shell=True)
