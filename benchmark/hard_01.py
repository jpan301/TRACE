# VULNERABLE: injection buried inside an if block
# harder to detect because the sink is conditional
from flask import request
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def get_user(request):
    user_id = request.args.get("id")
    role = request.args.get("role")
    if role == "admin":
        query = "SELECT * FROM users WHERE id = " + user_id
        cursor.execute(query)
        return cursor.fetchone()
    return None
