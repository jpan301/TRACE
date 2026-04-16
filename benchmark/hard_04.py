# VULNERABLE: 3-step variable chain before the sink
# taint has to be traced through 3 assignments
from flask import request
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def search(request):
    raw = request.args.get("q")          # step 1: user input
    term = raw                            # step 2: copy to new variable
    clause = "WHERE title = '" + term + "'"   # step 3: build clause
    query = "SELECT * FROM posts " + clause   # step 4: build full query
    cursor.execute(query)
    return cursor.fetchall()
