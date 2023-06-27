import psycopg2
import numpy as np
import io

def insert_image_as_blob(image_array, db_connection, table_name, column_name):
    # Convert image array to bytes
    image_bytes = image_array.tobytes()

    # Create a BytesIO object to hold the image data
    blob_data = io.BytesIO(image_bytes)

    # Establish a database connection
    conn = psycopg2.connect(db_connection)
    cursor = conn.cursor()

    try:
        # Open the blob file for reading
        with blob_data as blob_file:
            # Execute the INSERT query
            cursor.execute(f"INSERT INTO {table_name} ({column_name}) VALUES (%s)", (psycopg2.Binary(blob_file.read()),))

        # Commit the transaction
        conn.commit()
        print("Image blob inserted successfully!")
    except (psycopg2.DatabaseError, psycopg2.OperationalError) as e:
        # Rollback the transaction on error
        conn.rollback()
        print(f"Error inserting image blob: {e}")

    # Close the cursor and database connection
    cursor.close()
    conn.close()
