# VULNERABLE: escape function is applied but used incorrectly
# the escaped value is still interpolated into the query string
# LLM should recognize that escaping alone without parameterization is not safe
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def escape(value):
    return value.replace("'", "\\'")  # escaping quotes — but this can be bypassed

def get_user(username):
    safe = escape(username)
    query = "SELECT * FROM users WHERE name = '" + safe + "'"
    cursor.execute(query)   # still vulnerable — escaping is not parameterization
    return cursor.fetchone()
