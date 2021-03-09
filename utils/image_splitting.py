### Daniel Vogler and Philipp Schaedle
###
### split pictures into subcategory folders

import os
import sys
from shutil import copyfile

### load file with global parameter settings
from global_parameters import *

### basic information
# execute this script in a folder containing raw images
# the files are sorted into a new folder named after the raw image folder in the project directory
dataDir = os.getcwd()
baseDir = os.path.dirname(os.path.realpath(__file__))
mainDir = os.path.join(baseDir, os.path.basename(dataDir))
# if this script is executed in the project folder images are copied from a folder called "original_data/"
if dataDir == baseDir:
    dataDir = str( projectImages + "original_data/")
    mainDir = os.path.dirname(os.path.dirname(dataDir))

print("Process images in: ", dataDir)

if not os.path.exists(mainDir):
    os.makedirs(mainDir)
if not os.path.exists(mainDir + "/testing/"):
    os.makedirs(mainDir + "/testing/")
if not os.path.exists(mainDir + "/training/"):
    os.makedirs(mainDir + "/training/")
if not os.path.exists(mainDir + "/validation/"):
    os.makedirs(mainDir + "/validation/")

### find subdirectories to extract all categories
print("\n\n Find subdirectories and extract categories\n")

def get_immediate_subdirectories(dataDir):
    return [name for name in os.listdir(dataDir)
            if os.path.isdir(os.path.join(dataDir, name))]

nameDir = get_immediate_subdirectories(dataDir)
print("Categories: {}\n\n".format(nameDir))


### find pics in subdirectories
for category in nameDir:
    numPics = 0

    print("\t Category: {}\n".format(category))

    ### create folders in training/testing environment
    if not os.path.exists(mainDir + "/testing/" + category):
        os.makedirs(mainDir + "/testing/" + category)
    if not os.path.exists(mainDir + "/training/" + category):
        os.makedirs(mainDir + "/training/" + category)
    if not os.path.exists(mainDir + "/validation/" + category):
        os.makedirs(mainDir + "/validation/" + category)

    ### find and extract images in subfolders
    catDir = os.path.join(dataDir, category)
    print("\t\t Number of pictures found: {}\n\n".format( len( os.listdir( catDir ) ) ))

    test_val_sort = 0

    for file in os.listdir(catDir):

        filename = os.fsdecode(file)

        if filename.endswith(".png") or filename.endswith(".jpg") or filename.endswith(".JPG"):

            ### sort equally into testing and validation
            numPics +=1
            
            if numPics % percentage == 0: #put in testing
                test_val_sort += 1

                ### split test and validation images
                if (test_val_sort % 2) == 0:
                    copyfile(os.path.join(catDir, filename), os.path.join(mainDir, "validation", category, filename))
                else:
                    copyfile(os.path.join(catDir, filename), os.path.join(mainDir, "testing", category, filename))

            else:   #put in training
                copyfile(os.path.join(catDir, filename), os.path.join(mainDir, "training", category, filename))

            continue
        else:
            continue

print("DONE")
