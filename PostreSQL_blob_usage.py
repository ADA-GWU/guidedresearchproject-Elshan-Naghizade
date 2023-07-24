import psycopg2
import numpy as np
import io

def create_connection(db_connection):
    try:
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

def create_table(cursor, table_name, column_name):
    try:
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (id SERIAL PRIMARY KEY, {column_name} BYTEA)")
        print(f"Table '{table_name}' created successfully.")
    except (psycopg2.DatabaseError, psycopg2.OperationalError) as e:
        print(f"Error creating the '{table_name}' table: {e}")

def insert_image_as_blob(image_array, db_connection, table_name, column_name):
    image_bytes = image_array.tobytes()
    blob_data = io.BytesIO(image_bytes)
    conn = create_connection(db_connection)
    if not conn:
        return

    cursor = conn.cursor()

    try:
        create_table(cursor, table_name, column_name)

        with blob_data as blob_file:
            cursor.execute(f"INSERT INTO {table_name} ({column_name}) VALUES (%s)", (psycopg2.Binary(blob_file.read()),))

        conn.commit()
        print("Image blob inserted successfully!")
    except (psycopg2.DatabaseError, psycopg2.OperationalError) as e:
        conn.rollback()
        print(f"Error inserting image blob: {e}")
    finally:
        close_connection(conn, cursor)

def retrieve_image_blob(db_connection, table_name, column_name, image_id):
    conn = create_connection(db_connection)
    if not conn:
        return None

    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT {column_name} FROM {table_name} WHERE id = %s", (image_id,))
        binary_data = cursor.fetchone()[0]

        image_array = np.frombuffer(binary_data, dtype=np.uint8)
        return image_array
    except (psycopg2.DatabaseError, psycopg2.OperationalError) as e:
        print(f"Error retrieving image blob: {e}")
        return None
    finally:
        close_connection(conn, cursor)

def get_all_image_ids(db_connection, table_name):
    conn = create_connection(db_connection)
    if not conn:
        return []

    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT id FROM {table_name}")
        image_ids = [row[0] for row in cursor.fetchall()]
        return image_ids
    except (psycopg2.DatabaseError, psycopg2.OperationalError) as e:
        print(f"Error retrieving image IDs: {e}")
        return []
    finally:
        close_connection(conn, cursor)
