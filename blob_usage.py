import numpy as np
import sqlite3

def numpy_array_to_blob(image_array):
    # Convert the NumPy array to a binary string
    binary_string = image_array.tostring()

    # Connect to the database
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    # Create a table to store the blob
    cursor.execute("CREATE TABLE IF NOT EXISTS images (id INTEGER PRIMARY KEY, image BLOB)")

    # Insert the binary string into the database
    cursor.execute("INSERT INTO images (image) VALUES (?)", (binary_string,))

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

