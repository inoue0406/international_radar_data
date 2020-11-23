import os
import sys
import tempfile

import boto
from boto.s3.connection import S3Connection
from datetime import timedelta, datetime

import numpy as np
from matplotlib import pyplot as plt
import pandas as pd
import pyart

#Helper function for the search
def _nearestDate(dates, pivot):
    return min(dates, key=lambda x: abs(x - pivot))

def get_radar_from_aws(site, datetime_t):
    """
    Get the closest volume of NEXRAD data to a particular datetime.
    Parameters
    ----------
    site : string
        four letter radar designation
    datetime_t : datetime
        desired date time
    Returns
    -------
    radar : Py-ART Radar Object
        Radar closest to the queried datetime
    """

    #First create the query string for the bucket knowing
    #how NOAA and AWS store the data

    my_pref = datetime_t.strftime('%Y/%m/%d/') + site

    #Connect to the bucket

    conn = S3Connection(anon = True)
    bucket = conn.get_bucket('noaa-nexrad-level2')

    #Get a list of files

    bucket_list = list(bucket.list(prefix = my_pref))

    #we are going to create a list of keys and datetimes to allow easy searching

    keys = []
    datetimes = []

    #populate the list

    for i in range(len(bucket_list)):
        this_str = str(bucket_list[i].key)
        if 'gz' in this_str:
            endme = this_str[-22:-4]
            fmt = '%Y%m%d_%H%M%S_V0'
            dt = datetime.strptime(endme, fmt)
            datetimes.append(dt)
            keys.append(bucket_list[i])

        if this_str[-3::] == 'V06':
            endme = this_str[-19::]
            fmt = '%Y%m%d_%H%M%S_V06'
            dt = datetime.strptime(endme, fmt)
            datetimes.append(dt)
            keys.append(bucket_list[i])

    #find the closest available radar to your datetime

    closest_datetime = _nearestDate(datetimes, datetime_t)
    dtsec = closest_datetime - datetime_t
    dtsec = dtsec.total_seconds()
    index = datetimes.index(closest_datetime)
    if dtsec > 60.0*5:
        print('The data is too much apart: skip. dtsec=',dtsec)
        radar = np.nan
    else:
        localfile = tempfile.NamedTemporaryFile()
        keys[index].get_contents_to_filename(localfile.name)
        try:
            radar = pyart.io.read(localfile.name)
        except ValueError:
            print('Unable to read in file: ',localfile.name)
            radar = np.nan
    return radar,closest_datetime,dtsec

def dl_prep_NEXRAD(b_d,site,fcsv):
    # b_d is a datetime object

    base_date = b_d.strftime('%Y%m%d_%H%M%S')
    fmt = '%Y%m%d_%H%M%S' 
    b_d = datetime.strptime(base_date, fmt)

    print("obtaining data:",base_date)
    #my_radar,dtime,dtsec = get_radar_from_aws('KAMX',b_d )
    my_radar,dtime,dtsec = get_radar_from_aws(site,b_d)

    if type(my_radar) is not pyart.core.radar.Radar:
        print("no data: skipped")
        return

    # calc rainfall intensity
    rain = pyart.retrieve.est_rain_rate_z(my_radar)
    my_radar.add_field('rainfall', rain, replace_existing = True)

    # grid conversion
    # nlevel = 46
    # height = 15000 # in meters
    nlevel = 1
    height = 1000 # in meters
    ngrid = 200
    extent = 200000 # in meters
    dxy = 2*extent/ngrid # grid size in meters
    print("converting to grid: grid size[m]:",dxy)
    grids = pyart.map.grid_from_radars(
         my_radar, grid_shape=(nlevel, ngrid, ngrid),
        grid_limits=((0, height),(-extent, extent), (-extent, extent)),
        fields=['rainfall'], gridding_algo="map_gates_to_grid",
        weighting_function='BARNES')

    R0 = grids.fields["rainfall"]["data"]

    print("%s,%s,%f,%f,%f"% (b_d,dtime,dtsec,R0.mean(),R0.max()),file=fcsv,flush=True)

    # test write
    #for z in range(nlevel):
    #    zstr = "%03d" % z
    #    plt.imshow(R0[z,:,:].astype(np.float32),vmin=0,vmax=10,origin='lower')
    #    plt.savefig('../../result/NEXRAD/tstout/rain_figure_'+base_date+'_z'+zstr+'.png')
     
if __name__ == '__main__':
    # read case name from command line
    argvs = sys.argv
    argc = len(argvs)

    if argc != 4:
        print('Usage: python prep_NEXRAD.py setting site start_date')
        quit()

    setting = argvs[1]
    isite = int(argvs[2]) # site 0-155
    start_date = argvs[3]
    print("setting:",setting)
    print("site:",isite)
    print("date:",start_date)
    
    outfile_root = "../data/preprocessed/DWD_RYDL/"
    
    site_list=pd.read_csv("../src/NEXRAD/NEXRAD_site_list.csv",header=None)
    site_list=site_list[0].tolist()
    
    setting = "train"
    #setting = "valid"
    #site = "KTLX"
    site = site_list[isite]
    
    if setting == "train":
        # select 2015 and 2016 for training
        dates = pd.date_range(start=start_date+' 00:00', end='2016-12-31 22:00', freq='H')
    elif setting == "valid":
        # select 2017 for validation
        dates = pd.date_range(start='2017-01-01 00:00', end='2017-12-31 22:00', freq='H')
        
    fcsv = open("../data/preprocessed/NEXRAD/NEXRAD_list_precip_"+str(isite)+site+".csv","w")
    print("date,i,j,rain_mean,rain_max",file=fcsv)

    #first lets connect to the bucket
    #conn = S3Connection(anon = True)
    #bucket = conn.get_bucket('noaa-nexrad-level2')
    #as we can see there is a LOT we can do with a bucket!!!
    #dir(bucket)
    
    for n,date in enumerate(dates):
        print(date)
        base_date = date.to_pydatetime()
        dl_prep_NEXRAD(base_date,site,fcsv)

