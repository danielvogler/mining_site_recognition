# mining site recognition
Recognize mining sites from satellite data. Download images of satellite data from given coordinates.

## Structure
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

## Usage

### Satellite image download
1. Set up account with `https://www.sentinel-hub.com/` to be able to download images
2. Get instance_id [here](https://apps.sentinel-hub.com/dashboard/#/configurations)
3. Get client_id and client_secret when setting up an OAuth client [here](https://apps.sentinel-hub.com/dashboard/#/account/settings)
4. Save sentinelhub config file **sh_config.py** in **satellite_data_scraping/**. 
   ```
   from sentinelhub import SHConfig
  
   config = SHConfig()

   config.instance_id = '{instance_id_here}'
   config.sh_client_id = '{sh_client_id_here}'
   config.sh_client_secret = '{sh_client_secret_here}'

   config.save()
   ```
   More infos here: [Link](https://sentinelhub-py.readthedocs.io/en/latest/configure.html)
5. Setup dimensions, coordinates, bands etc. of image locations in **`image_config_{username}.py`**. Do not modify **image_config.py**!
6. Run **sentinelhub_image_download.py**

### classification
1. Set-up folder **/{project_name}/** (e.g. **/infrared_images/**) for classification of images with given settings
2. Save all images in folder **/{project_name}/original_data/**
3. Execute **image_splitting.py** in **/{project_name}/** to sort images into train, validation and test folders
4. Copy all files from folder **classification/** into **/{project_name}/
5. Adjust settings in **global_parameters.py** (now in **/{project_name}/**) if needed
6. Train model by running **classification.py**
7. Re-load model and view results with **load_classification.py**
