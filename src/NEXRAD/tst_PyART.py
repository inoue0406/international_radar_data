import boto
from boto.s3.connection import S3Connection
from datetime import timedelta, datetime
import os
import pyart
from matplotlib import pyplot as plt
import tempfile
import numpy as np

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

    localfile = tempfile.NamedTemporaryFile()
    keys[index].get_contents_to_filename(localfile.name)
    radar = pyart.io.read(localfile.name)
    return radar,closest_datetime,dtsec

if __name__ == '__main__':
    #first lets connect to the bucket
    conn = S3Connection(anon = True)
    bucket = conn.get_bucket('noaa-nexrad-level2')

    #as we can see there is a LOT we can do with a bucket!!!
    dir(bucket)

    base_date = "20161006_192700"
    fmt = '%Y%m%d_%H%M%S' 
    b_d = datetime.strptime(base_date, fmt)

    print("obtaining data:",base_date)
    my_radar,dtime,dtsec = get_radar_from_aws('KAMX',b_d )

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

    print(b_d,dtime,dtsec,R0.mean(),R0.max())

    # test write
    for z in range(nlevel):
        zstr = "%03d" % z
        plt.imshow(R0[z,:,:].astype(np.float32),vmin=0,vmax=10,origin='lower')
        plt.savefig('../../result/NEXRAD/tstout/rain_figure_'+base_date+'_z'+zstr+'.png')
     
    import pdb;pdb.set_trace()
    
    max_lat = 27
    min_lat = 24
    min_lon = -81
    max_lon = -77

    lal = np.arange(min_lat, max_lat, .5)
    lol = np.arange(min_lon, max_lon, .5)

    display = pyart.graph.RadarMapDisplay(my_radar)
    fig = plt.figure(figsize = [10,8])
    display.plot_ppi_map('reflectivity', sweep = 0, resolution = 'c',
                         vmin = -8, vmax = 64, mask_outside = False,
                         cmap = pyart.graph.cm.NWSRef,
                         min_lat = min_lat, min_lon = min_lon,
                         max_lat = max_lat, max_lon = max_lon,
                         lat_lines = lal, lon_lines = lol)
