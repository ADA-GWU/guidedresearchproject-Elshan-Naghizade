import cv2
import numpy as np
import os

def get_file_paths(directory):
    return [os.path.join(root, file_name) 
            for root, _, files in os.walk(directory) 
            for file_name in files]

def save_as_numpy_array(data, path):
    np.save(path, data)
    return path, str(data.dtype)

def load_image(image_path):
    return cv2.imread(image_path), os.path.splitext(image_path)[1][1:]

def get_image_dimensions(image):
    return image.shape[0], image.shape[1], image.shape[2]

def compute_color_histogram(image):
    hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    return cv2.normalize(hist, hist).flatten()

def detect_edges(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return cv2.Canny(gray, 30, 100)

def detect_corners(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return np.int0(cv2.goodFeaturesToTrack(gray, 25, 0.01, 10))

def extract_features(image_path):
    image, ext = load_image(image_path)
    if image is None:
        return 999
    height, width, channels = get_image_dimensions(image)
    array_path, array_dtype = save_as_numpy_array(np.array(image), f'{image_path}_arr.npy')
    hist_path, _ = save_as_numpy_array(compute_color_histogram(image), f'{image_path}_hist.npy')
    edges_path, _ = save_as_numpy_array(detect_edges(image), f'{image_path}_edges.npy')
    corners_path, _ = save_as_numpy_array(detect_corners(image), f'{image_path}_corners.npy')
    return ((image_path, height, width, channels, ext), (array_path, array_dtype), (hist_path, edges_path, corners_path))

def generate_sql_inserts(num, features):
    main_sql = f"INSERT INTO Main_tab_ ({num}, Relative_Location_, Height_, Width_, Channels_, File_Type_, Image_id_) VALUES {features[0]};"
    array_sql = f"INSERT INTO Array_Tab_ ({num}, Array_location_, Array_type_, Image_id_) VALUES {features[1]};"
    feature_sql = f"INSERT INTO Feature_Tab_ ({num}, Histogram_, Edges_, Corners_, Image_id_) VALUES {features[2]};"
    return main_sql, array_sql, feature_sql

def write_to_file(inserts):
    with open('Inserts.sql', 'w') as f:
        f.write('\n'.join(inserts) + '\n')

image_loc = '222.png'
features = extract_features(image_loc)
num = 8888
inserts = generate_sql_inserts(num, features)
write_to_file(inserts)
