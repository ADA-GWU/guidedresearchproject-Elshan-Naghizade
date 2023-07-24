import cv2
import numpy as np
import os
import sqlite3

class ImageFeatureDataset:
    def __init__(self, db_name='image_features.db'):
        self.db_name = db_name
        self.conn = self.create_connection()
        self.cursor = self.conn.cursor()
        self.create_tables()

    def __del__(self):
        self.close_connection()

    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_name)
            return conn
        except sqlite3.Error as e:
            print(f"Error connecting to the database: {e}")
            return None

    def close_connection(self):
        try:
            if self.conn:
                self.cursor.close()
                self.conn.close()
        except sqlite3.Error as e:
            print(f"Error closing the database connection: {e}")

    def create_tables(self):
        try:
            self.cursor.execute("CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY, path TEXT, height INTEGER, width INTEGER, channels INTEGER, extension TEXT)")
            self.cursor.execute("CREATE TABLE IF NOT EXISTS features (id INTEGER PRIMARY KEY, image_id INTEGER, array_path TEXT, array_dtype TEXT, hist_path TEXT, edges_path TEXT, corners_path TEXT)")
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating the tables: {e}")

    def insert_image_and_features(self, image_path, image_data):
        try:
            binary_string = image_data.tobytes()
            array_path, array_dtype = self.save_as_numpy_array(image_data, f'{image_path}_arr.npy')
            hist_path, _ = self.save_as_numpy_array(self.compute_color_histogram(image_data), f'{image_path}_hist.npy')
            edges_path, _ = self.save_as_numpy_array(self.detect_edges(image_data), f'{image_path}_edges.npy')
            corners_path, _ = self.save_as_numpy_array(self.detect_corners(image_data), f'{image_path}_corners.npy')
            self.cursor.execute("INSERT INTO images (path, height, width, channels, extension) VALUES (?, ?, ?, ?, ?)",
                                (image_path, image_data.shape[0], image_data.shape[1], image_data.shape[2], os.path.splitext(image_path)[1][1:]))
            image_id = self.cursor.lastrowid
            self.cursor.execute("INSERT INTO features (image_id, array_path, array_dtype, hist_path, edges_path, corners_path) VALUES (?, ?, ?, ?, ?, ?)",
                                (image_id, array_path, array_dtype, hist_path, edges_path, corners_path))
            self.conn.commit()
        except sqlite3.Error as e:
            self.conn.rollback()
            print(f"Error inserting image and features: {e}")

    def get_all_images(self):
        try:
            self.cursor.execute("SELECT path FROM images")
            return [row[0] for row in self.cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error retrieving image paths: {e}")
            return []

    def get_image_and_features(self, image_path):
        try:
            self.cursor.execute("SELECT image.id, path, height, width, channels, extension, array_path, array_dtype, hist_path, edges_path, corners_path FROM images "
                                "JOIN features ON images.id = features.image_id WHERE path=?", (image_path,))
            row = self.cursor.fetchone()
            if row:
                image_id, _, height, width, channels, extension, array_path, array_dtype, hist_path, edges_path, corners_path = row
                image_data = self.blob_to_numpy_array(array_path, array_dtype, (height, width, channels))
                hist_data = self.blob_to_numpy_array(hist_path, np.float32)
                edges_data = self.blob_to_numpy_array(edges_path, np.uint8)
                corners_data = self.blob_to_numpy_array(corners_path, np.int0)
                return image_data, hist_data, edges_data, corners_data, extension
            else:
                return None, None, None, None, None
        except sqlite3.Error as e:
            print(f"Error retrieving image and features: {e}")
            return None, None, None, None, None

    def save_as_numpy_array(self, data, path):
        try:
            np.save(path, data)
            return path, str(data.dtype)
        except Exception as e:
            print(f"Error saving data as numpy array: {e}")
            return None

    def blob_to_numpy_array(self, blob_path, dtype, shape=None):
        try:
            with open(blob_path, 'rb') as f:
                binary_string = f.read()
            if shape:
                return np.frombuffer(binary_string, dtype=dtype).reshape(shape)
            else:
                return np.frombuffer(binary_string, dtype=dtype)
        except Exception as e:
            print(f"Error loading binary data to NumPy array: {e}")
            return None
