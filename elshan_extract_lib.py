import cv2
import numpy as np
import os

def get_file_paths(directory):
    file_paths = []
    for root, dirs, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_paths.append(file_path)
    return file_paths

    
def extract_features(image_path):
    # Get the extension of the file
    _, ext = os.path.splitext(image_path)
    ext_ = ext[1:]

    # Load the image with OpenCV
    image = cv2.imread(image_path)
    image_array = np.array(image)
    i_name = image_path+'_arr.npy'
    np.save(i_name, image_array)
    image_dtype = str(image.dtype)

    if image is not None:
        # Get the dimensions of the image
        dimensions = image.shape

        # Height, width, number of channels in image
        height = image.shape[0]
        width = image.shape[1]
        channels = image.shape[2]

        # Compute color histogram
        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist,hist).flatten()
        h_name = image_path+'_hist.npy'
        np.save(h_name, hist)
        # Convert image to grayscale for edge and corner detection
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Edge detection (Canny)
        edges = cv2.Canny(gray,30,100)
        e_name = image_path+'_edges.npy'
        np.save(e_name, edges)

        # Corner detection (Shi-Tomasi)
        corners = cv2.goodFeaturesToTrack(gray,25,0.01,10)
        corners = np.int0(corners)
        c_name = image_path+'_corners.npy'
        np.save(c_name, corners)
        main_tab = tuple([image_path, height, width, channels, ext_])
        array_tab = tuple([i_name, image_dtype])
        feature_tab = tuple([h_name, e_name, c_name])
        return main_tab, array_tab, feature_tab
    else:
        return 999

image_loc = '222.png'
t1, t2, t3 = extract_features(image_loc)

num = 8888

main_sql = "INSERT INTO Main_tab_ ("+str(num)+f", Relative_Location_, Height_, Width_, Channels_, File_Type_, Image_id_) VALUES {t1};"
array_sql = "INSERT INTO Array_Tab_ ("+str(num)+f", Array_location_, Array_type_, Image_id_) VALUES {t2};"
feature_sql = "INSERT INTO Feature_Tab_ ("+str(num)+f", Histogram_, Edges_, Corners_, Image_id_) VALUES {t3};"

with open('Inserts.sql', 'w') as f:
    f.write(main_sql + '\n')
    f.write(array_sql + '\n')
    f.write(feature_sql + '\n')
