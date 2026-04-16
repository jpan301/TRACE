# VULNERABLE: injection inside a for loop
# the sink is called multiple times with tainted input
from flask import request
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def get_users(request):
    ids = request.args.get("ids", "").split(",")
    results = []
    for uid in ids:
        query = "SELECT * FROM users WHERE id = " + uid
        cursor.execute(query)
        results.append(cursor.fetchone())
    return results
