# SAFE: obvious sanitizer function wraps the input before use
# static engine sees param -> sanitize_input(param) -> query -> execute
# LLM should recognize sanitize_input as a sanitizer and suppress
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def sanitize_input(value):
    # strips dangerous characters — in practice this may not be enough
    # but the name clearly signals intent
    return value.replace("'", "''").replace(";", "")

def search_users(name):
    safe_name = sanitize_input(name)
    query = "SELECT * FROM users WHERE name = '" + safe_name + "'"
    cursor.execute(query)
    return cursor.fetchall()
