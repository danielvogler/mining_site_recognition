### Daniel Vogler
### save augmented images

from keras.preprocessing.image import ImageDataGenerator
import os
import glob
import matplotlib.pyplot as plt
import numpy as np

### plot example images from chosen generator
def createAugmentedImages(
    augmentedImages,
    save_to_dir,
    steps_per_epoch,
    target_size,
    batch_size,
    class_mode,
    color_mode,
    save_prefix,
    rescale,
    shear_range,
    zoom_range,
    rotation_range,
    width_shift_range,
    height_shift_range,
    horizontal_flip,
    vertical_flip):

    ### create main augmentation directory
    if not os.path.exists(save_to_dir):
        os.makedirs(save_to_dir)

    ### augmented datagenerator
    augmented_datagen = ImageDataGenerator(
        rescale = rescale,
        shear_range = shear_range,
        zoom_range = zoom_range,
        rotation_range = rotation_range,
        width_shift_range = width_shift_range,
        height_shift_range = height_shift_range,
        horizontal_flip = horizontal_flip,
        vertical_flip = vertical_flip)

    ### Use target_size parameter to convert images to 32x32 pixels
    augmented_set = augmented_datagen.flow_from_directory(
        augmentedImages,
        target_size = target_size,
        batch_size = batch_size,
        class_mode = class_mode,
        color_mode = color_mode,
        save_to_dir = save_to_dir,
        save_prefix = save_prefix)

    ### remove augmented images from previous runs
    augmented_image_folder = glob.glob(save_to_dir)
    for fo in augmented_image_folder:
        file = glob.glob(f'{fo}/*')
        for f in file:
            os.remove(f)

    ### execute image generator
    for i in range(steps_per_epoch):
        ### saves one batch of images each
        augmented_set.next()

    print('\n\nSaved augmented image examples to: \n\t{}\n\n'.format(save_to_dir))
    return

# ### plot example images from chosen generator
# def createAugmentedImages(augmentedImages,save_to_dir):

#     ### augmented datagenerator
#     augmented_datagen = ImageDataGenerator(
#         rescale = rescale,
#         shear_range = shear_range,
#         zoom_range = zoom_range,
#         rotation_range = rotation_range,
#         width_shift_range = width_shift_range,
#         height_shift_range = height_shift_range,
#         horizontal_flip = horizontal_flip,
#         vertical_flip = vertical_flip)

#     ### Use target_size parameter to convert images to 32x32 pixels
#     augmented_set = augmented_datagen.flow_from_directory(
#         augmentedImages,
#         target_size = target_size,
#         batch_size = batch_size,
#         class_mode = class_mode,
#         save_to_dir = save_to_dir,
#         save_prefix = save_prefix)

#     ### remove augmented images from previous runs
#     augmented_image_folder = glob.glob(save_to_dir)
#     for fo in augmented_image_folder:
#         file = glob.glob(f'{fo}/*')
#         for f in file:
#             os.remove(f)

#     ### execute image generator
#     for i in range(steps_per_epoch):
#         ### saves one batch of images each
#         augmented_set.next()



# current_batch = next(augmented_set)
# fig, m_axs = plt.subplots(1, 32, figsize = (26, 6))
# for img, class_index_one_hot, ax1 in zip(current_batch[0], current_batch[1], m_axs.T):
#     ax1.imshow(img)
#     class_index = np.argmax(class_index_one_hot)
#     ax1.set_title(str(class_index) + ':' + index_to_classes[class_index])
#     ax1.axis('off')
