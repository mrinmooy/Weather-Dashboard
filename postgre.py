import psycopg2

# Replace placeholders with your actual server details and credentials
conn = psycopg2.connect(
    dbname="postgres",
    user="mrinmoy",
    password="RsA%9V27",
    host="backend-logging.postgres.database.azure.com",
    port='5432',
    sslmode='require'  # This is required for Azure
)
cur = conn.cursor()

# Example query
cur.execute("SELECT version();")
record = cur.fetchone()
print("You are connected to - ", record)

cur.close()
conn.close()
