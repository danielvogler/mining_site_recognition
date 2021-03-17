#
# global parameters for project
#

import pathlib
file_path = pathlib.Path(__file__).parent.absolute()

###
### image sorting (training/test/validation)
###
validation_split = 0.2 
test_split = 0.1
training_split = 1 - validation_split - test_split

###
### input properties
###
numberOfCategories = 2
epoch_number = 20  ### iteration over data (defined by steps_per_epoch).
steps_per_epoch = 100  ### Number of steps (batches) from gen / epoch
batch_size = 32 ### Number of samples per gradient update.
validation_steps = 10   ### # of steps (batches) from valid_data gen / epoch
max_queue_size = 10 ### Maximum size for the generator queue.
class_mode = 'categorical'  ### binary or categorical
shuffle = False
img_width, img_height = 64, 64#32, 32# 100, 100 ### dimensions of our images.
target_size = (img_width, img_height)

###
### project parameters
###
projectImages = str( str(file_path) + "/")
trainingImages = str(projectImages + "training/")
testingImages = str(projectImages + "testing/")
validationImages = str(projectImages + "validation/")
augmentedImages = str(projectImages + "training/")
save_augmented_images_TF = False
subDirectories = ['Mine', 'NotMine']
resultsDirectory = 'results/'
save_to_dir=str(projectImages+'augmented_images/')
save_prefix= str('aug_pxl'+str(img_width)+'x'+str(img_height)+'_')

###
### augmentation parameters
###
rotation_range=0
width_shift_range=0.0
height_shift_range=0.0
rescale=-1./255
shear_range=0.2
zoom_range=0.2
horizontal_flip=True
vertical_flip=True
# tf.keras.preprocessing.image.ImageDataGenerator.flow_from_directory()
# color_mode: One of "grayscale", "rgb", "rgba". Default: "rgb".
# Whether the images will be converted to have 1, 3, or 4 channels.
color_mode='rgb'
