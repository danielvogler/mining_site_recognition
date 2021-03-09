### daniel vogler
### sentinelhub satellite data download
### additonal info at https://sentinelhub-py.readthedocs.io

from sentinelhub import SHConfig

config = SHConfig()

if config.sh_client_id == '' or config.sh_client_secret == '':
    print("Warning! To use Sentinel Hub Process API, please provide the credentials (client ID and client secret).")

import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
import pandas
import math
import importlib
from random import randrange
from PIL import Image
from datetime import datetime

from sentinelhub import MimeType, CRS, BBox, SentinelHubRequest, SentinelHubDownloadClient, \
    DataCollection, bbox_to_dimensions, DownloadRequest

start_time = datetime.now()

'''
Settings
'''

### load username
un = os.getlogin()

### check for local config file
try:
    cnfg = importlib.import_module( str("image_config_"+un) )

### otherwise use global repo config
except:
    cnfg = importlib.import_module("image_config")

### load config
mining_locations = cnfg.mining_locations
bands = cnfg.bands
bands_id = cnfg.bands_id
resolution = cnfg.resolution
bb_size = cnfg.bb_size
save_to = cnfg.save_to
region_id = cnfg.region_id
categories = cnfg.categories

### coordinates to load
ml = pandas.read_csv(mining_locations)
ml = ml.dropna()

### construct filename accoring to gid
def construct_gid_str(save_to, mine_id, bands_id, bb_size, region_id, file_id):
    ### naming convention
    ### global identifier --> gidABCDEFG_lat...
    ### A: nonMine/mine : 0/1
    ### B: band: normal (0), infrared (1)
    ### C: edge length in km (1, 2, 3 ...)
    ### D: region identifier: operating_mines (a), NT (b), QLD (c), WA (d), S_WA (z)
    ### EFG: 3 digit file id
    gid_str = str(save_to + \
        mine_id + \
        str(bands_id) + \
        str(int(bb_size/1000)) + \
        region_id)

    return gid_str


### compute bounding box in degree lat/lon
def bounding_box(lat,lon,bb_size):

    ### distance for 1 degree at given latitude
    delta_lat = 111132.954 - 559.822*math.cos(2*math.radians(lat)) \
                + 1.175*math.cos(4*math.radians(lat))

    ### distance for 1 degree at given longitude
    delta_lon = 111132.954 * math.cos( math.radians(lat) )

    ### degree for given bounding box size
    bb_size_lat = bb_size / delta_lat
    bb_size_lon = bb_size / delta_lon

    ### Set image geometry
    bounding_box = [lon-bb_size_lon/2.0,lat-bb_size_lat/2.0, 
        lon+bb_size_lon/2.0,lat+bb_size_lat/2.0]

    return bounding_box


### image plotting function
def plot_image(image, factor=1.0, clip_range = None, **kwargs):

    fig = plt.figure()
    plt.axis('off')
    plt.imshow(image * factor)


### construct sample order for sentinel request string
def construct_band_str(bands):
    band_str = "sample.%s" %bands[-1]

    for i in range(1,len(bands)):
        band_str += ", sample.%s" % bands[-1-i]

    return band_str


### create evaluation script according to requested bands
def evaluation_script(bands):

    band_str = construct_band_str(bands)

    evalscript = """
        //VERSION=3

        function setup() {
            return {
                input: [{
                    bands: %s
                }],
                output: {
                    bands: %i
                }
            };
        }

        function evaluatePixel(sample) {
            return [%s];
        }
    """ % (bands, len(bands), band_str)

    return evalscript


### request image data from sentinelhub
def request_image(lat,lon,bands,resolution,bb_size,file_str):

    ### bounding box at lat/lon
    image_geometry = bounding_box(lat, lon, bb_size)

    ### define image geometry
    image_bbox = BBox(bbox=image_geometry, crs=CRS.WGS84)
    image_size = bbox_to_dimensions(image_bbox, resolution=resolution)
    ### make sure image is same length on each side
    image_size_ave = int((image_size[0] + image_size[1])/2)
    image_size = (image_size_ave, image_size_ave)
    image_size = ( int(bb_size/resolution), int(bb_size/resolution) )

    print(f'Image shape at {resolution}m resolution: {image_size} pixels')

    ### bands to use
    evalscript = evaluation_script(bands)

    ### image request with ir bands
    request_color = SentinelHubRequest(
        evalscript=evalscript,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L1C,
                time_interval=('2020-06-01', '2020-12-30'),
                mosaicking_order='leastCC'
            )
        ],
        responses=[
            SentinelHubRequest.output_response('default', MimeType.PNG)
        ],
        bbox=image_bbox,
        size=image_size,
        config=config
    )

    ### plot image with least cloud cover
    # plot_image(request_color.get_data()[0], factor=3.5/255, clip_range=(0,1))
    # plt.savefig(file_str,bbox_inches='tight',pad_inches = 0)

    ### download data
    true_color_imgs = request_color.get_data()
    image = true_color_imgs[0]

    # print(f'Returned data is of type = {type(true_color_imgs)} and length {len(true_color_imgs)}.')
    # print(f'Single element in the list is of type {type(true_color_imgs[-1])} and has shape {true_color_imgs[-1].shape}')
    # print(f'Image type: {image.dtype}')

    image = Image.fromarray(image)
    image.save(file_str)


# loop over the mine locations
for i in range(len(ml['Latitude'])):

    print("\nLoading coordinate index:", ml.index[i])

    ### mines and non-mines
    for j in categories:

        ### lon,lat of lower left and upper right corner
        lat = ml['Latitude'].iloc[i]
        lon = ml['Longitude'].iloc[i]

        if j == 0:
            lat += randrange(20,100)*(-1)**randrange(2)/100
            lon += randrange(20,100)*(-1)**randrange(2)/100

        ### options for mine/non-mine
        mine_id = str(j)
        ### image index in region
        file_id = str(ml.index[i]).zfill(4)
        ### gid string for database
        gid_str = construct_gid_str(save_to, mine_id, bands_id, bb_size, region_id, file_id)


        file_str = str( gid_str + \
            file_id + \
            "_-_lat" + \
            str("{:.6f}".format(lat)) + \
            "_lon" + \
            str("{:.6f}".format(lon)) + \
            ".png")
        
        ### load image specified by bb
        request_image(lat, lon, bands, resolution, bb_size, file_str)

print("\nTotal execution time:", datetime.now() - start_time)
