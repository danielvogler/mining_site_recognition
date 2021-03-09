from osgeo import gdal

import os, sys, glob
import numpy as np
import pylab as pl 


# find current location where tif files are stored and create new folder with extension '_processed' to write png output
# this file is executed from tif image folder
foldername = os.path.basename(os.getcwd())
process_folder = os.path.join('..', foldername+'_processed')
if not os.path.exists(process_folder) and len(glob.glob('*.tif'))>0:
    print('create output folder', process_folder)
    os.mkdir(process_folder)

for filename in glob.glob('*.tif'):
    print(filename)
    # load file
    ds = gdal.Open(filename)  
    print(ds.RasterCount, ds.RasterYSize, ds.RasterXSize)
    nda=ds.ReadAsArray()
    print(nda.shape)

    rgb = np.zeros([nda.shape[1],nda.shape[2],3])

    # check
    if 1:
        rgb[:,:,0] = nda[0,:,:]/np.amax(nda[0,:,:])
        rgb[:,:,1] = nda[1,:,:]/np.amax(nda[1,:,:])
        rgb[:,:,2] = nda[2,:,:]/np.amax(nda[2,:,:])
    
    # Original method to convert
    div = 20000.
    if 0:
        rgb[:,:,0] = nda[0,:,:]/div
        rgb[:,:,1] = nda[1,:,:]/div
        rgb[:,:,2] = nda[2,:,:]/div

    outfile = filename.replace('.tif', '.png')
    # write png file
    pl.imsave(os.path.join(process_folder, outfile), rgb)

print("done")
