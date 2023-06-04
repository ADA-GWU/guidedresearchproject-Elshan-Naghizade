# Elshan Naghizade Guided Research

## Tentative Plan:
I am planning to build a python library which would extract metadata from image datasets to transform them into tables and bring them into a SQL-like query-ready format. Given an image of a popular format (for instance, png or jpeg) this python module would extract useful features to eliminate the need to manually develop data-loaders for preprocessing. Those features might be (not limited to) size, edges, corners, blobs, color-maps, etc.

## Expected Features:
Automatically extracting the features universal for most image datasets and transforming them into a structured form would allow using conventional SQL queries on those metadata tables significantly cutting down the time spent on developing case-specific dataloaders and, most importantly, bringing SQL’s flexibility and speed.
A further step that might be taken later is to test the generated metadata tables in scalable NoSQL databases.

Building the “scaffold” of application (simple feature extraction, like width, height, colormap, interception-based cropping queries) and to test it with MySQL.
Additionally, Sobel and Prewitt edges, Harris corner detectors and some other sophisticated features to be made available within
SQL queries on metadata tables.

## Practical Appeal:
Computer Vision engineers spend a significant amount of time to cleanse and transform their image datasets into a state suitable for the model to be developed. Having simple SQL queries to snap through the datasets would simplify the automation of data-preprocessing requiring less manual interventions into the dataset itself, while interacting with the metadata itself.
