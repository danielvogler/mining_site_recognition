# mining site recognition
Recognize mining sites from satellite data.

### Files
- bulk_conversion.py: Conversion of satelite data from .tif to .png 
- classify_categories.py: Train network on image data
- global_parameters.py: Contains hyperparameters etc. to make it easier to test settings on different datasets
- image_splitting.py: Split data sets into train/valid/test 
- load_classification.py: Load all saved model data and plot results
- save_augemented_images: To enable the writing of augmented images for inspection
