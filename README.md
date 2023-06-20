# Elshan Naghizade Guided Research

## Tentative Plan:
I am planning to build a python library which would extract metadata from image datasets to transform them into tables and bring them into a SQL-like query-ready format. Given an image of a popular format (for instance, png or jpeg) this python module would extract useful features to eliminate the need to manually develop data-loaders for preprocessing. Those features might be (not limited to) size, edges, corners, blobs, color-maps, etc.

## Under Progress:
- Using blobs to store images instead of relative OS paths (Recommended by Dr. Hasanov)
- Will be connecting the codebase to PostreSQL (the initial plan was to utilize MySQL)
- Modify the input/output flow of the class to conform with general python library guidelines (Recommended by Dr. Kaisler)

## Current Version's Documentation:
This Python script performs feature extraction on images and generates SQL INSERT statements to populate database tables. Here's a breakdown of what the script does:

1. File Path Gathering
The function get_file_paths(directory) takes a directory path as input and returns a list of all file paths in the directory and its subdirectories. This is achieved through the use of os.walk(), which recursively traverses through the directory tree.

2. Image Feature Extraction
The function extract_features(image_path) takes the path of an image file as input and performs the following tasks:

Loads the image with OpenCV.
Extracts and saves the image array as a numpy array.
Computes the color histogram of the image and saves it as a numpy array.
Converts the image to grayscale for edge and corner detection.
Detects edges using the Canny method and saves them as a numpy array.
Detects corners using the Shi-Tomasi method and saves them as a numpy array.
All features are saved as numpy arrays with a corresponding name to their image file. The function returns three tuples containing information for insertion into the Main_tab_, Array_Tab_, and Feature_Tab_ tables.

3. SQL Statement Generation
The script then generates SQL INSERT statements using the tuples returned by extract_features(). Each tuple is formatted as the VALUES clause in an INSERT statement for the corresponding table.

The SQL statements are as follows:

main_sql: This statement inserts the image location, height, width, number of channels, and file type into the Main_tab_ table.
array_sql: This statement inserts the location of the saved numpy array and the array data type into the Array_Tab_ table.
feature_sql: This statement inserts the locations of the saved histogram, edges, and corners numpy arrays into the Feature_Tab_ table.
An arbitrary number (num) is also included as the first field in each INSERT statement.

4. SQL Statement Saving
The SQL INSERT statements are written to a single .sql file named 'Inserts.sql'. Each statement is on a new line for readability.

## Expected Features:
Automatically extracting the features universal for most image datasets and transforming them into a structured form would allow using conventional SQL queries on those metadata tables significantly cutting down the time spent on developing case-specific dataloaders and, most importantly, bringing SQL’s flexibility and speed.
A further step that might be taken later is to test the generated metadata tables in scalable NoSQL databases.

Building the “scaffold” of application (simple feature extraction, like width, height, colormap, interception-based cropping queries) and to test it with MySQL.
Additionally, Sobel and Prewitt edges, Harris corner detectors and some other sophisticated features to be made available within
SQL queries on metadata tables.

## Practical Appeal:
Computer Vision engineers spend a significant amount of time to cleanse and transform their image datasets into a state suitable for the model to be developed. Having simple SQL queries to snap through the datasets would simplify the automation of data-preprocessing requiring less manual interventions into the dataset itself, while interacting with the metadata itself.
