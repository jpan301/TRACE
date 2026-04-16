# SAFE: looks like percent formatting injection but is actually safe
# the %s here is a SQL placeholder passed as second argument, not Python % operator
from flask import request
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def search_users(request):
    name = request.args.get("name")
    # this looks like it could be vulnerable but the tuple argument makes it safe
    sql = "SELECT * FROM users WHERE name LIKE %s"
    cursor.execute(sql, (f"%{name}%",))  # parameterized — the f-string is in the tuple, not the SQL
    return cursor.fetchall()
