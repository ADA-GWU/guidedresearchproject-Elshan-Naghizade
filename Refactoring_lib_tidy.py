import cv2
import numpy as np
import os

# Function to get all file paths in a directory
def get_file_paths(directory):
    return [os.path.join(root, file_name) 
            for root, _, files in os.walk(directory) 
            for file_name in files]

# Function to save data as numpy array
def save_as_numpy_array(data, path):
    try:
        np.save(path, data)
        return path, str(data.dtype)
    except Exception as e:
        print(f"Error saving data as numpy array: {e}")
        return None

# Function to load an image and its extension
def load_image(image_path):
    try:
        image = cv2.imread(image_path)
        return image, os.path.splitext(image_path)[1][1:]
    except Exception as e:
        print(f"Error loading image: {e}")
        return None, None

# Function to get the dimensions of an image
def get_image_dimensions(image):
    if image is not None:
        return image.shape[0], image.shape[1], image.shape[2]
    return None, None, None

# Function to compute color histogram of an image
def compute_color_histogram(image):
    try:
        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        return cv2.normalize(hist, hist).flatten()
    except Exception as e:
        print(f"Error computing color histogram: {e}")
        return None

# Function to perform edge detection on an image
def detect_edges(image):
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.Canny(gray, 30, 100)
    except Exception as e:
        print(f"Error detecting edges: {e}")
        return None

# Function to perform corner detection on an image
def detect_corners(image):
    try:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return np.int0(cv2.goodFeaturesToTrack(gray, 25, 0.01, 10))
    except Exception as e:
        print(f"Error detecting corners: {e}")
        return None

# Function to extract features from an image
def extract_features(image_path):
    image, ext = load_image(image_path)
    if image is None:
        return None
    height, width, channels = get_image_dimensions(image)
    array_path_info = save_as_numpy_array(np.array(image), f'{image_path}_arr.npy')
    hist_path_info = save_as_numpy_array(compute_color_histogram(image), f'{image_path}_hist.npy')
    edges_path_info = save_as_numpy_array(detect_edges(image), f'{image_path}_edges.npy')
    corners_path_info = save_as_numpy_array(detect_corners(image), f'{image_path}_corners.npy')

    if None in [array_path_info, hist_path_info, edges_path_info, corners_path_info]:
        return None
    array_path, array_dtype = array_path_info
    hist_path, _ = hist_path_info
    edges_path, _ = edges_path_info
    corners_path, _ = corners_path_info
    return ((image_path, height, width, channels, ext), (array_path, array_dtype), (hist_path, edges_path, corners_path))

# Function to generate SQL insert statements
def generate_sql_inserts(num, features):
    main_sql = f"INSERT INTO Main_tab_ (Num, Relative_Location_, Height_, Width_, Channels_, File_Type_, Image_id_) VALUES {num}, %s, %s, %s, %s, %s, %s);"
    array_sql = f"INSERT INTO Array_Tab_ (Num, Array_location_, Array_type_, Image_id_) VALUES {num}, %s, %s, %s);"
    feature_sql = f"INSERT INTO Feature_Tab_ (Num, Histogram_, Edges_, Corners_, Image_id_) VALUES {num}, %s, %s, %s, %s);"
    return main_sql, array_sql, feature_sql

# Function to write SQL insert statements to a file
def write_to_file(inserts):
    try:
        with open('Inserts.sql', 'w') as f:
            for insert in inserts:
                f.write(insert + '\n')
        print("SQL insert statements written to 'Inserts.sql'.")
    except Exception as e:
        print(f"Error writing SQL insert statements to file: {e}")

# Using the above functions to extract image features and generate SQL insert statements
if __name__ == "__main__":
    image_loc = 'path/to/your/image.png'  # Replace this with the path to your image
    features = extract_features(image_loc)
    if features is not None:
        num = 8888
        inserts = generate_sql_inserts(num, features)
        write_to_file(inserts)

