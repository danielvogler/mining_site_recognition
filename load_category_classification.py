### Daniel Vogler
### load classification result

import os
import json
from keras.models import model_from_json
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator
import csv
from itertools import zip_longest
import matplotlib.pyplot as plt


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
    augmentedImages = str(projectImages + "training/")


### enter some example images below to test classification performance
nmTest1 = './individualTests/imageCopernicus_nonMine_0210.png'
nmTest2 = './individualTests/imageCopernicus_nonMine_0225.png'
nmTest3 = './individualTests/imageCopernicus_nonMine_0228.png'
mTest1 = './individualTests/imageCopernicus0026.png'
mTest2 = './individualTests/imageCopernicus0033.png'
mTest3 = './individualTests/imageCopernicus0040.png'

### Returns a compiled model identical to the previous one
model = load_model(projectImages + resultsDirectory + 'model.h5')

### evaluate loaded model on test data
### config the model with losses and metrics
model.compile(
    optimizer='rmsprop',
    loss='categorical_crossentropy',
    metrics=['categorical_accuracy'])

### Create test set
test_datagen = ImageDataGenerator(rescale = rescale)

### Use target_size parameter to convert images to 32x32 pixels
test_set = test_datagen.flow_from_directory(
    testingImages,
    target_size = (img_width, img_height),
    batch_size = batch_size,
    class_mode = class_mode,
    color_mode = color_mode,
    shuffle = shuffle)

### SCORES
### Evaluate the model on the test data using `evaluate`
### (You can pass a Dataset instance directly to the methods fit(), evaluate(), and predict():)
scores = model.evaluate(test_set)
print("Model evaluate:")
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
print("SUMMARY--")
print(model.summary())


### Test with individual image
import numpy as np
from keras.preprocessing import image

### test images
def testImagePredictor(testImage):

    print("\n Image prediction for file: {}".format(testImage))

    ### load and adjust test imagetulip
    test_image = image.load_img( testImage , target_size = (img_width, img_height) )
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis=0)

    ### predict test image according to model
    result = model.predict(test_image)
    test_set.class_indices

    ### evaluate results
    if result[0][0] >= .5:
        prediction = 'mine'
    elif result[0][1] >= .5:
        prediction = 'non-mine'
    else:
        prediction = 'failed'

    print(prediction)

    return result

### test some images
### result[0][0] is probability of image being xyz
### index is 0 because xyz is first category listed
### (1)
# result = testImagePredictor(projectImages + nmTest1)
### (2)
# result = testImagePredictor(projectImages + nmTest2)
### (3)
# result = testImagePredictor(projectImages + nmTest3)
### (4)
# result = testImagePredictor(projectImages + mTest1)
### (5)
# result = testImagePredictor(projectImages + mTest2)
### (6)
# result = testImagePredictor(projectImages + mTest3)

###
### LABEL RESULTS
###

### plot figures for probabilities of different classes
def plotTestResults(labels, filenames, test_prediction):
    ### loop through classes
    class_type = []
    label_names =  []
    for classes in range(np.size(test_prediction,1)):
        prob = []
        for i, k in zip([f.split('/')[0] for f in filenames], test_prediction):
            if i==labels[classes]:
                prob.append(k)
        prob = np.array(prob)
        class_type.append(prob[:, classes])
        label_names.append(labels[classes])

        plt.figure()
        ### Visualize the probability distribution for each class
        bins = np.linspace(0, 1, 11)
        plt.hist([test_prediction[:,classes], prob[:, classes]], bins)
        plt.title( str('Probability - ' + labels[classes] ) )
        plt.ylabel('Frequency [-]')
        plt.xlabel('Probability [-]')
        plt.legend(['Prediction', labels[classes]])
        plt.savefig( str(projectImages + resultsDirectory + 'probability_-_' + labels[classes] + '.png') )

    plt.figure()
    ### Visualize the probability distribution for each class
    bins = np.linspace(0, 1, 11)
    plt.hist(class_type, bins)
    plt.title('Probability')
    plt.ylabel('Frequency [-]')
    plt.xlabel('Probability [-]')
    plt.legend(label_names)
    plt.savefig( str(projectImages + resultsDirectory + 'probability_-_cum.png') )

### rest test generator
test_set.reset()
### predict generator to evaluate test images
test_prediction=model.predict_generator(test_set,verbose=1)
### extract maximum label value
predicted_class_indices=np.argmax(test_prediction,axis=1)
### add probability to which a mine or notmine is found
predicted_class_probability = np.max(test_prediction,axis=1)
### Extract labels of tested images
labels = (test_set.class_indices)
### create dict to assign class labels to predictions
labels = dict((v,k) for k,v in labels.items())
### assign class label to predictions
predictions = [labels[k] for k in predicted_class_indices]
### Extract filenames of tested images
filenames=test_set.filenames
### plot predicted probabilities
plotTestResults(labels, filenames, test_prediction)
### lists to write to file
dataToWrite = [predictions, predicted_class_probability, filenames]
dataToWriteZipped = zip_longest(*dataToWrite, fillvalue = '')
### write predictions to file
with open(str(projectImages + resultsDirectory + 'predictions.csv'), 'w', newline='') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerows(dataToWriteZipped)

myfile.close()

### SCORES
print("Model evaluate:")
scores = model.evaluate(test_set)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

plt.show()
