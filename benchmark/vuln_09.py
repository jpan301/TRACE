from flask import request
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def get_profile(request):
    uid = request.args.get("uid")
    where_clause = "id = " + uid
    query = "SELECT * FROM profiles WHERE " + where_clause
    cursor.execute(query)
    return cursor.fetchone()
