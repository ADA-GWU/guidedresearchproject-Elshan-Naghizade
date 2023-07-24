import cv2
import numpy as np
import os
import sqlite3
import psycopg2
from contextlib import contextmanager

class ImageFeatureDataset:
    def __init__(self, db_name='image_features.db', db_connection=None):
        self.db_name = db_name
        self.db_connection = db_connection
        self.create_tables()

    @contextmanager
    def connect(self):
        conn = psycopg2.connect(self.db_connection) if self.db_connection else sqlite3.connect(self.db_name)
        try:
            yield conn.cursor()
        finally:
            conn.close()

    def create_tables(self):
        with self.connect() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY, path TEXT, height INTEGER, width INTEGER, channels INTEGER, extension TEXT)")
            cursor.execute("CREATE TABLE IF NOT EXISTS features (id INTEGER PRIMARY KEY, image_id INTEGER, array BLOB, hist BLOB, edges BLOB, corners BLOB)")
            cursor.connection.commit()

    def compute_color_histogram(self, image):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1, 2], None, (8, 8, 8), [0, 180, 0, 256, 0, 256])
        cv2.normalize(hist, hist)
        return hist.flatten()

    def detect_edges(self, image):
        return cv2.Canny(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), 30, 100)

    def detect_corners(self, image):
        gray = np.float32(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
        return np.int0(cv2.goodFeaturesToTrack(gray, 100, 0.01, 10))

    def insert_image_and_features(self, image_path):
        image_data = cv2.imread(image_path)
        with self.connect() as cursor:
            cursor.execute("INSERT INTO images (path, height, width, channels, extension) VALUES (?, ?, ?, ?, ?)",
                           (image_path, image_data.shape[0], image_data.shape[1], image_data.shape[2], os.path.splitext(image_path)[1][1:]))
            image_id = cursor.lastrowid
            cursor.execute("INSERT INTO features (image_id, array, hist, edges, corners) VALUES (?, ?, ?, ?, ?)",
                           (image_id,
                            self.numpy_array_to_blob(image_data),
                            self.numpy_array_to_blob(self.compute_color_histogram(image_data)),
                            self.numpy_array_to_blob(self.detect_edges(image_data)),
                            self.numpy_array_to_blob(self.detect_corners(image_data))))
            cursor.connection.commit()

    def update_image_and_features(self, image_path):
        image_data = cv2.imread(image_path)
        with self.connect() as cursor:
            cursor.execute("UPDATE images SET path = ?, height = ?, width = ?, channels = ?, extension = ? WHERE path = ?",
                           (image_path, image_data.shape[0], image_data.shape[1], image_data.shape[2], os.path.splitext(image_path)[1][1:], image_path))
            cursor.execute("UPDATE features SET array = ?, hist = ?, edges = ?, corners = ? WHERE image_id = (SELECT id FROM images WHERE path = ?)",
                           (self.numpy_array_to_blob(image_data),
                            self.numpy_array_to_blob(self.compute_color_histogram(image_data)),
                            self.numpy_array_to_blob(self.detect_edges(image_data)),
                            self.numpy_array_to_blob(self.detect_corners(image_data)),
                            image_path))
            cursor.connection.commit()

    def delete_image_and_features(self, image_path):
        with self.connect() as cursor:
            cursor.execute("DELETE FROM features WHERE image_id = (SELECT id FROM images WHERE path = ?)", (image_path,))
            cursor.execute("DELETE FROM images WHERE path = ?", (image_path,))
            cursor.connection.commit()

    def get_all_images(self):
        with self.connect() as cursor:
            cursor.execute("SELECT path FROM images")
            return [row[0] for row in cursor.fetchall()]

    def get_image_and_features(self, image_path):
        with self.connect() as cursor:
            cursor.execute("SELECT images.id, path, height, width, channels, extension, array, hist, edges, corners FROM images "
                           "JOIN features ON images.id = features.image_id WHERE path=?", (image_path,))
            row = cursor.fetchone()
            if row:
                image_id, _, height, width, channels, extension, array, hist, edges, corners = row
                image_data = self.blob_to_numpy_array(array, (height, width, channels))
                hist_data = self.blob_to_numpy_array(hist)
                edges_data = self.blob_to_numpy_array(edges)
                corners_data = self.blob_to_numpy_array(corners)
                return image_data, hist_data, edges_data, corners_data, extension
            return None, None, None, None, None

    def numpy_array_to_blob(self, array):
        return sqlite3.Binary(array.tobytes())

    def blob_to_numpy_array(self, blob, shape=None):
        array = np.frombuffer(blob, dtype=np.float32)
        return array.reshape(shape) if shape else array
