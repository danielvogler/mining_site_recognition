### Daniel Vogler and Philipp Schaedle
###
### split pictures into subcategory folders

import os
import sys
from shutil import copyfile
from math import floor

### load file with global parameter settings
from global_parameters import *

### basic information
# execute this script in a folder containing raw images
# the files are sorted into a new folder named after the raw image folder in the project directory
data_dir = os.getcwd()
base_dir = os.path.dirname(os.path.realpath(__file__))
main_dir = os.path.join(base_dir, os.path.basename(data_dir))
# if this script is executed in the project folder images are copied from a folder called "original_data/"
if data_dir == base_dir:
    data_dir = str( projectImages + "original_data/")
    main_dir = os.path.dirname(os.path.dirname(data_dir))

print("Process images in: ", data_dir)

if not os.path.exists(main_dir):
    os.makedirs(main_dir)
if not os.path.exists(main_dir + "/testing/"):
    os.makedirs(main_dir + "/testing/")
if not os.path.exists(main_dir + "/training/"):
    os.makedirs(main_dir + "/training/")
if not os.path.exists(main_dir + "/validation/"):
    os.makedirs(main_dir + "/validation/")

### find subdirectories to extract all categories
print("\n\n Find subdirectories and extract categories\n")

def get_immediate_subdirectories(data_dir):
    return [name for name in os.listdir(data_dir)
            if os.path.isdir(os.path.join(data_dir, name))]

name_dir = get_immediate_subdirectories(data_dir)
print("Categories: {}\n\n".format(name_dir))


### find pics in subdirectories
for category in name_dir:
    numPics = 0

    print("\t Category: {}\n".format(category))

    ### create folders in training/testing environment
    if not os.path.exists(main_dir + "/testing/" + category):
        os.makedirs(main_dir + "/testing/" + category)
    if not os.path.exists(main_dir + "/training/" + category):
        os.makedirs(main_dir + "/training/" + category)
    if not os.path.exists(main_dir + "/validation/" + category):
        os.makedirs(main_dir + "/validation/" + category)

    ### find and extract images in subfolders
    cat_dir = os.path.join(data_dir, category)
    print("\t\tNumber of pictures found: {}\n".format( len( os.listdir( cat_dir ) ) ))

    ### list all images in category folder
    dir_images = os.listdir(cat_dir)
    total_cat_images = len(dir_images)

    ### determine fraction of images for train, valid, test
    training_images = floor(training_split*total_cat_images)
    validation_images = floor(validation_split*total_cat_images)
    test_images = floor(test_split*total_cat_images)

    print('\t\tSorting into')
    print('\t\tTraining images: {}'.format(training_images) )
    print('\t\tValidation images: {}'.format(validation_images) )
    print('\t\tTest images: {}\n\n'.format(test_images) )

    ### go through all images
    for f in range(len(dir_images)):

        filename = os.fsdecode(dir_images[f])

        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".JPG"):

            ### sort equally into testing and validation
            numPics +=1
            
            ### sort and copy into train, valid, test folders
            if f <= training_images:
                copyfile(os.path.join(cat_dir, filename), os.path.join(main_dir, "training", category, filename))

            elif training_images < f < (training_images + validation_images):
                copyfile(os.path.join(cat_dir, filename), os.path.join(main_dir, "validation", category, filename))

            else:
                copyfile(os.path.join(cat_dir, filename), os.path.join(main_dir, "testing", category, filename))

            continue
        else:
            continue

print("DONE")
