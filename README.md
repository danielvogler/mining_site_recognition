# mining site recognition
Recognize mining sites from satellite data.

### Structure
* **classification/**
  * classification.py: Train network on image data
  * global_parameters.py: Contains hyperparameters etc. to make it easier to test settings on different datasets
  * load_classification.py: Load all saved model data and plot results
  * save_augemented_images: To enable the writing of augmented images for inspection
* **gid_database/**
  * assign_GID_database.py: Rename tifs image files and assign global identifier
  * restructure_GID_database.py: Restructure the database and dissect the global identifiers into columns
* **satellite_data_scraping/**
  * image_config.py: Settings for images
  * sentinelhub_image_download.py: Download images via sentinelhub
* **utils/**
  * bulk_conversion.py: Conversion of satelite data from .tif to .png
  * image_splitting.py: Split data sets into train/valid/test
