# Elshan Naghizade Guided Research

## Tentative Plan:
I am planning to build a python library which would extract data and features from image datasets to transform them into tables and bring them into a SQL-like query-ready format. Given an image of a popular format (for instance, png or jpeg) this python module would extract useful features to eliminate the need to manually develop data-loaders for preprocessing. Those features might be (not limited to) size, edges, corners, blobs, color-maps, etc.

## Under Progress:
- Using blobs to store images instead of relative OS paths (Recommended by Dr. Hasanov)
- Will be connecting the codebase to PostreSQL (the initial plan was to utilize MySQL)
- Modify the input/output flow of the class to conform with general python library guidelines (Recommended by Dr. Kaisler)

## Current Version's Documentation:
#### init(self, db_name='image_features.db', db_connection=None)
This is the constructor for the ImageFeatureDataset class. It initializes the class with the database name or database connection string. It also calls the create_tables() method to ensure that the necessary tables exist in the database.

#### connect(self)
This is a context manager for handling the database connections. It opens a connection to the specified database and yields a cursor for executing SQL statements. After execution, it ensures that the connection is closed.

#### create_tables(self)
This method creates the necessary tables in the database if they do not exist. It creates two tables: images and features.

#### compute_color_histogram(self, image)
Computes a color histogram of the input image in HSV color space and returns it as a 1D array.

#### detect_edges(self, image)
Detects edges in the input image using the Canny edge detection algorithm and returns a binary image with detected edges.

#### detect_corners(self, image)
Detects corners in the input image using the Shi-Tomasi corner detection algorithm and returns a binary image with detected corners.

#### insert_image_and_features(self, image_path)
Takes an image path as input, computes features of the image (color histogram, edges, corners), and inserts them into the database.

#### update_image_and_features(self, image_path)
Takes an image path as input, recomputes features of the image (color histogram, edges, corners), and updates them in the database.

#### delete_image_and_features(self, image_path)
Deletes the record of the specified image and its associated features from the database.

#### get_all_images(self)
Retrieves the paths of all images stored in the database.

#### get_image_and_features(self, image_path)
Retrieves the features of the specified image from the database.

#### numpy_array_to_blob(self, array)
Converts a numpy array into a binary format that can be stored in the database.

#### blob_to_numpy_array(self, blob, shape=None)
Converts a binary format back into a numpy array. The shape of the original array must be provided if it was not a 1D array.

## Expected Features:
Automatically extracting the features universal for most image datasets and transforming them into a structured form would allow using conventional SQL queries on those metadata tables significantly cutting down the time spent on developing case-specific dataloaders and, most importantly, bringing SQL’s flexibility and speed.
A further step that might be taken later is to test the generated metadata tables in scalable NoSQL databases.

Building the “scaffold” of application (simple feature extraction, like width, height, colormap, interception-based cropping queries) and to test it with MySQL.
Additionally, Sobel and Prewitt edges, Harris corner detectors and some other sophisticated features to be made available within
SQL queries on metadata tables.

## Practical Appeal:
Computer Vision engineers spend a significant amount of time to cleanse and transform their image datasets into a state suitable for the model to be developed. Having simple SQL queries to snap through the datasets would simplify the automation of data-preprocessing requiring less manual interventions into the dataset itself, while interacting with the metadata itself.
