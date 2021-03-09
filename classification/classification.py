# Daniel Vogler, Philipp Schaedle
#
# Sort images from source folder categories into
# testing and training folders

from keras.models import Sequential
from keras.layers import Convolution2D
from keras.layers import MaxPooling2D
from keras.layers import Flatten
from keras.layers import Dropout
from keras.layers import Dense
from keras.utils.np_utils import to_categorical
from keras.preprocessing.image import ImageDataGenerator
from IPython.display import display
from PIL import Image

import json
import matplotlib.pyplot as plt
import sys
import os

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")

### load file with global parameter settings
from global_parameters import *

### define to work locally or globally
mainDir = os.getcwd()
baseDir = os.path.dirname(os.path.realpath(__file__))
# check if globally
if mainDir != baseDir:
    print("Work globally")
    projectImages = str( str(mainDir) + "/")
    trainingImages = str(projectImages + "training/")
    testingImages = str(projectImages + "testing/")
    validationImages = str(projectImages + "validation/")
    augmentedImages = str(projectImages + "training/")


### declare and intialize sequential model
classifier = Sequential()

### 1. convolutional input layer
###   32 feature maps with a size of 3x3 and
###   rectifier activation function (relu==rectified linear unit)
classifier.add(Convolution2D(32,3,3,
    input_shape=(img_width,img_height,3),
    activation='relu'))
### 2. Dropout layer at 10%
classifier.add(Dropout(.1))
### 3. Max pool layer with size 2x2
classifier.add(MaxPooling2D(pool_size = (2,2) ) )
### 4. Flatten layer
classifier.add(Flatten())
### 5. fully connected layer with 1024 units and a relu
classifier.add(Dense(1024, activation='relu'))
### 6. fully connected layer with 512 units and a relu
classifier.add(Dense(512, activation='relu'))
### 7. fully connected layer with 256 units and a relu
classifier.add(Dense(256, activation='relu'))
# ### 8. fully connected layer with 128 units and a relu
# classifier.add(Dense(128, activation='relu'))
### 9. fully connected layer with #ofCategories units and a softmax
classifier.add(Dense(numberOfCategories, activation='softmax'))

### compile classifier
classifier.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['categorical_accuracy'])

###
### DATA GENERATORS
###

### Train datagenerator
train_datagen = ImageDataGenerator(
    rescale = rescale,
    shear_range = shear_range,
    zoom_range = zoom_range,
    rotation_range = rotation_range,
    width_shift_range = width_shift_range,
    height_shift_range = height_shift_range,
    horizontal_flip = horizontal_flip,
    vertical_flip = vertical_flip)

### Validation datagenerator
validation_datagen = ImageDataGenerator(rescale=rescale)

### Test datagenerator
test_datagen = ImageDataGenerator(rescale=rescale)

### generate TRAINING dataset based on augmentation parameters
training_set = train_datagen.flow_from_directory(
    trainingImages,
    target_size = target_size,
    batch_size = batch_size,
    class_mode = class_mode,
    color_mode = color_mode)#,
    # save_to_dir = save_to_dir,
    # save_prefix = save_prefix)


### generate VALIDATION dataset based on augmentation parameters
validation_set = validation_datagen.flow_from_directory(
    validationImages,
    target_size = target_size,
    batch_size = batch_size,
    class_mode = class_mode,
    color_mode = color_mode)

### generate TEST dataset based on augmentation parameters
test_set = test_datagen.flow_from_directory(
    testingImages,
    target_size = target_size,
    batch_size = batch_size,
    class_mode = class_mode,
    color_mode = color_mode)

nb_train_samples = len(training_set.filenames)
num_classes = len(training_set.class_indices)

### get class labels for training data
train_labels = training_set.classes

###
### Train data and save performance
###
history = classifier.fit_generator(
    training_set,
    steps_per_epoch = steps_per_epoch,
    epochs = epoch_number,
    max_queue_size = max_queue_size,#)#,
    validation_data = test_set,
    validation_steps = validation_steps)


###
### save model
###
if not os.path.exists(projectImages + resultsDirectory):
    os.makedirs(projectImages + resultsDirectory)

### serialize model to JSON
with open(projectImages + resultsDirectory + "model_architecture.json", "w") as json_file:
    json_file.write( classifier.to_json() )
print("\n Saved model architecture to disk")

### serialize weights to HDF5
classifier.save_weights(projectImages + resultsDirectory + "model_weights.h5")
print("\n Saved model weights to disk")

### Creates a HDF5 file 'my_model.h5'
classifier.save(projectImages + resultsDirectory + 'model.h5')
print("\n Saved model to disk")


###
### PLOT model results
###

### Visualize the models accuracy
plt.figure()
plt.plot(history.history['categorical_accuracy'])
if 'val_categorical_accuracy' in history.history:
    plt.plot(history.history['val_categorical_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train','Val'],loc='upper left')
plt.savefig( str(projectImages + resultsDirectory + 'model_accuracy.png') )

### Visualize the models loss
plt.figure()
plt.plot(history.history['loss'])
if 'val_loss' in history.history:
    plt.plot(history.history['val_loss'])
plt.title('Model loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(['Train','Val'], loc='upper right')
plt.savefig( str(projectImages + resultsDirectory + 'model_loss.png') )

#plt.show()


### save some example augmented images
from save_augmented_images import createAugmentedImages

### comment this if you do not want to save example augmented images
if save_augmented_images_TF:
    createAugmentedImages(augmentedImages,save_to_dir,
        steps_per_epoch,(img_width, img_height),batch_size,class_mode,color_mode,
        save_prefix,rescale,shear_range,zoom_range,rotation_range,
        width_shift_range,height_shift_range,horizontal_flip,vertical_flip)


### Summarize scores
scores = classifier.evaluate(test_set)
print("SUMMARY--")
print(classifier.summary())
print("\n%s: %.2f%%" % (classifier.metrics_names[1], scores[1]*100))


exit()
