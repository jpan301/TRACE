# SAFE: looks suspicious but is actually safe
# has variables named "query" and calls cursor.execute
# but the user input never reaches the SQL string
from flask import request
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def get_user(request):
    user_id = request.args.get("id")   # user input
    query = "SELECT * FROM users"       # hardcoded query, no user input
    cursor.execute(query)               # safe — query has no user data in it
    all_users = cursor.fetchall()
    # user_id is used here for filtering in Python, not in SQL
    return [u for u in all_users if str(u[0]) == user_id]
