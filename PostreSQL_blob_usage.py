import psycopg2
import numpy as np
import io

def create_connection(db_connection):
    try:
        # Establish a database connection
        conn = psycopg2.connect(db_connection)
        return conn
    except (psycopg2.DatabaseError, psycopg2.OperationalError) as e:
        print(f"Error connecting to the database: {e}")
        return None

def close_connection(conn, cursor=None):
    try:
        if cursor:
            cursor.close()
        conn.close()
        print("Database connection closed.")
    except (psycopg2.DatabaseError, psycopg2.OperationalError) as e:
        print(f"Error closing the database connection: {e}")

def insert_image_as_blob(image_array, db_connection, table_name, column_name):
    # Convert image array to bytes
    image_bytes = image_array.tobytes()

    # Create a BytesIO object to hold the image data
    blob_data = io.BytesIO(image_bytes)

    # Create a database connection
    conn = create_connection(db_connection)
    if not conn:
        return

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
    finally:
        # Close the cursor and database connection
        close_connection(conn, cursor)
