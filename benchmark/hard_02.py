# VULNERABLE: variable name reused — looks safe at first glance
# user_id gets reassigned but the second assignment is still tainted
from flask import request
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def get_user(request):
    user_id = "default"           # looks like a safe hardcoded value
    user_id = request.args.get("id")   # but then immediately overwritten with user input
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)
    return cursor.fetchone()
