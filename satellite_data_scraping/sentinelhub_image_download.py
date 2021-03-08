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

from sentinelhub import MimeType, CRS, BBox, SentinelHubRequest, SentinelHubDownloadClient, \
    DataCollection, bbox_to_dimensions, DownloadRequest

'''
Settings
'''

### coordinates to load
mining_locations = '../../mining_site_recognition_internal/mining_locations/mining_location_coordinate_files/mining_database_-_western_australia_reduced_coord.csv'
ml = pandas.read_csv(mining_locations)

### set bands and create evaluation string
bands = ["B02", "B03", "B04"]
bands = ["B06", "B08", "B11"]

# size of bounding box for image sampling
image_bb_size = 0.0166*2

### image resolution in m
resolution = 10

### window bounding box size [m]
bb_size = 1000


### compute bounding box in degree lat/lon
def bounding_box(lat,lon,bb_size):

    ### earth radius
    R = 6378.137

    ### distance for 1 degree at given latitude
    delta_lat = 111132.954 - 559.822*math.cos(2*math.radians(lat)) + 1.175*math.cos(4*math.radians(lat))

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
    """
    Utility function for plotting RGB images.
    """
    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(15, 15))
    if clip_range is not None:
        ax.imshow(np.clip(image * factor, *clip_range), **kwargs)
    else:
        ax.imshow(image * factor, **kwargs)
    ax.set_xticks([])
    ax.set_yticks([])


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
def request_image(lat,lon,bands,resolution,bb_size):

    ### bounding box at lat/lon
    image_geometry = bounding_box(lat, lon, bb_size)

    ### define image geometry
    image_bbox = BBox(bbox=image_geometry, crs=CRS.WGS84)
    image_size = bbox_to_dimensions(image_bbox, resolution=resolution)

    print(f'Image shape at {resolution} m resolution: {image_size} pixels')

    ### bands to use
    evalscript = evaluation_script(bands)

    ### image request with ir bands
    request_color = SentinelHubRequest(
        evalscript=evalscript,
        input_data=[
            SentinelHubRequest.input_data(
                data_collection=DataCollection.SENTINEL2_L1C,
                time_interval=('2020-06-01', '2020-06-30'),
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
    plot_image(request_color.get_data()[0], factor=3.5/255, clip_range=(0,1))
    plt.show()

    ### download data
    true_color_imgs = request_color.get_data()

    print(f'Returned data is of type = {type(true_color_imgs)} and length {len(true_color_imgs)}.')
    print(f'Single element in the list is of type {type(true_color_imgs[-1])} and has shape {true_color_imgs[-1].shape}')

    image = true_color_imgs[0]
    print(f'Image type: {image.dtype}')


# loop over the mine locations
for i in range(len(ml['Latitude'])):

    ### lon,lat of lower left and upper right corner
    lat = ml['Latitude'].iloc[i]
    lon = ml['Longitude'].iloc[i]
    
    ### load image specified by bb
    request_image(lat,lon,bands,resolution,bb_size)
