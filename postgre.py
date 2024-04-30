import psycopg2
from datetime import datetime

# Establish the connection
def create_connection():
    return psycopg2.connect(
        dbname="logs",
        user="mrinmoy",
        password="RsA%9V27",
        host="backend-logging.postgres.database.azure.com",
        port='5432',
        sslmode='require'
    )

# Create the weather table if it doesn't exist
def create_table():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            city_name VARCHAR(255),
            temperature DECIMAL(5, 2),
            description VARCHAR(255),
            report_time TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

# Insert data into the weather table
def insert_data(city_name, temperature, description):
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO weather (city_name, temperature, description)
        VALUES (%s, %s, %s);
    """, (city_name, temperature, description))
    conn.commit()
    cur.close()
    conn.close()

# Read all entries from the weather table
def read_all_entries():
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM weather;")
    records = cur.fetchall()
    for record in records:
        print(record)
    cur.close()
    conn.close()

# Create the table (if it does not exist)
# create_table()

# Example usage of inserting data
# insert_data('San Francisco', 17.5, 'Foggy')
# insert_data('Guna', 30.0, 'Rainy')

# Reading and printing all entries from the table
read_all_entries()
