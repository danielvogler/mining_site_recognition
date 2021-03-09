### configuration file
### to use local settings:
### copy image_config.py to image_config_{username}.py

### coordinates to load
mining_locations = '../../mining_site_recognition_internal/mining_locations/mining_location_coordinate_files/mining_database_-_western_australia_reduced_coord.csv'

### set bands and create evaluation string
### band combination identifier (0)
# bands_id = 0
# bands = ["B02", "B03", "B04"]
### band combination identifier (1)
bands_id = 1
bands = ["B06", "B08", "B11"]

### image resolution in m
resolution = 10

### window bounding box size [m]
bb_size = 4000

### region identifier: operating_mines (a), NT (b), QLD (c), WA (d), S_WA (z)
region_id = 'd'

### do non-mine images as well: (1) yes; (0) no
categories = [0, 1]

### save folder
save_to = "../../mining_site_recognition_internal/mining_locations/mining_location_image_files/mining_database_-_western_australia_reduced/original_data/"