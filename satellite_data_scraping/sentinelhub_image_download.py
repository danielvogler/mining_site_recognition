### sentinelhub satellite data download
### https://sentinelhub-py.readthedocs.io

from sentinelhub import SHConfig

config = SHConfig()

if config.sh_client_id == '' or config.sh_client_secret == '':
    print("Warning! To use Sentinel Hub Process API, please provide the credentials (client ID and client secret).")

import os
import datetime
import numpy as np
import matplotlib.pyplot as plt

from sentinelhub import MimeType, CRS, BBox, SentinelHubRequest, SentinelHubDownloadClient, \
    DataCollection, bbox_to_dimensions, DownloadRequest

### lon,lat of lower left and upper right corner
koolan_island_openpit = [123.7,-16.2, 123.8, -16.1]

### image resolution in m
resolution = 10

### define geometry
koolan_island_bbox = BBox(bbox=koolan_island_openpit, crs=CRS.WGS84)
koolan_island_size = bbox_to_dimensions(koolan_island_bbox, resolution=resolution)

print(f'Image shape at {resolution} m resolution: {koolan_island_size} pixels')

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

### pull true color image
evalscript_true_color = """
    //VERSION=3

    function setup() {
        return {
            input: [{
                bands: ["B02", "B03", "B04"]
            }],
            output: {
                bands: 3
            }
        };
    }

    function evaluatePixel(sample) {
        return [sample.B04, sample.B03, sample.B02];
    }
"""

### initialize sentinelhub request
request_true_color = SentinelHubRequest(
    evalscript=evalscript_true_color,
    input_data=[
        SentinelHubRequest.input_data(
            data_collection=DataCollection.SENTINEL2_L1C,
            time_interval=('2020-06-12', '2020-06-13'),
        )
    ],
    responses=[
        SentinelHubRequest.output_response('default', MimeType.PNG)
    ],
    bbox=koolan_island_bbox,
    size=koolan_island_size,
    config=config
)

### download data
true_color_imgs = request_true_color.get_data()


print(f'Returned data is of type = {type(true_color_imgs)} and length {len(true_color_imgs)}.')
print(f'Single element in the list is of type {type(true_color_imgs[-1])} and has shape {true_color_imgs[-1].shape}')


image = true_color_imgs[0]
print(f'Image type: {image.dtype}')

### image request with least cloud cover
request_true_color = SentinelHubRequest(
    evalscript=evalscript_true_color,
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
    bbox=koolan_island_bbox,
    size=koolan_island_size,
    config=config
)

### plot image with least cloud cover
plot_image(request_true_color.get_data()[0], factor=3.5/255, clip_range=(0,1))
plt.show()
