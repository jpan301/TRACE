# SAFE: parameter is validated against a fixed whitelist before use
# static engine flags because column_name flows into query string
# LLM should recognize whitelist validation as protection
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

ALLOWED_COLUMNS = {"name", "email", "created_at", "status"}

def get_column(column_name):
    if column_name not in ALLOWED_COLUMNS:
        raise ValueError(f"invalid column: {column_name}")
    query = f"SELECT {column_name} FROM users"
    cursor.execute(query)
    return cursor.fetchall()
