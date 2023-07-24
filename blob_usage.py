import numpy as np
import sqlite3

def create_connection(db_name):
    try:
        # Establish a database connection
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
        # Create a table to store the blob if it doesn't exist
        cursor.execute("CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY, image BLOB)")
        print("Table 'images' created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating the 'images' table: {e}")

def numpy_array_to_blob(image_array, db_name='your_database.db'):
    try:
        # Convert the NumPy array to a binary string
        binary_string = image_array.tobytes()

        # Create a database connection
        conn = create_connection(db_name)
        if not conn:
            return

        cursor = conn.cursor()

        # Create the images table if it doesn't exist
        create_images_table(cursor)

        # Insert the binary string into the database
        cursor.execute("INSERT INTO images (image) VALUES (?)", (sqlite3.Binary(binary_string),))

        # Commit the transaction and close the connection
        conn.commit()
        print("Image blob inserted successfully!")
    except sqlite3.Error as e:
        # Rollback the transaction on error
        conn.rollback()
        print(f"Error inserting image blob: {e}")
    finally:
        # Close the cursor and database connection
        close_connection(conn, cursor)

def blob_to_numpy_array(db_name='your_database.db'):
    try:
        # Create a database connection
        conn = create_connection(db_name)
        if not conn:
            return None

        cursor = conn.cursor()

        # Retrieve the image blob from the database
        cursor.execute("SELECT image FROM images WHERE id = (SELECT MAX(id) FROM images)")
        binary_string = cursor.fetchone()[0]

        # Convert the binary string to a NumPy array
        image_array = np.frombuffer(binary_string, dtype=np.uint8)

        # Close the cursor and database connection
        close_connection(conn, cursor)

        # Reshape the NumPy array to its original shape (Modify this based on your image shape)
        # image_shape = (height, width, channels)
        # image_array = image_array.reshape(image_shape)

        return image_array
    except sqlite3.Error as e:
        print(f"Error retrieving image blob: {e}")
        return None
