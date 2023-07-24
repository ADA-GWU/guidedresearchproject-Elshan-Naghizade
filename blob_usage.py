import numpy as np
import sqlite3

def create_connection(db_name):
    try:
        conn = sqlite3.connect(db_name)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to the database: {e}")
        return None

def close_connection(conn, cursor=None):
    try:
        if cursor:
            cursor.close()
        conn.close()
        print("Database connection closed.")
    except sqlite3.Error as e:
        print(f"Error closing the database connection: {e}")

def create_images_table(cursor):
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY, image BLOB)")
    except sqlite3.Error as e:
        print(f"Error creating the 'images' table: {e}")

def numpy_array_to_blob(image_array, db_name='your_database.db'):
    try:
        binary_string = image_array.tobytes()
        conn = create_connection(db_name)
        if not conn:
            return

        cursor = conn.cursor()
        create_images_table(cursor)

        cursor.execute("INSERT INTO images (image) VALUES (?)", (sqlite3.Binary(binary_string),))
        conn.commit()
        print("Image blob inserted successfully!")
    except sqlite3.Error as e:
        conn.rollback()
        print(f"Error inserting image blob: {e}")
    finally:
        close_connection(conn, cursor)

def blob_to_numpy_array(db_name='your_database.db'):
    try:
        conn = create_connection(db_name)
        if not conn:
            return None

        cursor = conn.cursor()

        cursor.execute("SELECT image FROM images WHERE id = (SELECT MAX(id) FROM images)")
        binary_string = cursor.fetchone()[0]

        image_array = np.frombuffer(binary_string, dtype=np.uint8)

        close_connection(conn, cursor)

        return image_array
    except sqlite3.Error as e:
        print(f"Error retrieving image blob: {e}")
        return None
