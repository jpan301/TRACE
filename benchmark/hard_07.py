# SAFE: user input is converted to int then used in parameterized query
# double protection — int() conversion AND parameterized query
from flask import request
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def get_user(request):
    try:
        user_id = int(request.args.get("id", 0))  # int() makes injection impossible
    except ValueError:
        return None
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    return cursor.fetchone()
