from flask import request
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def get_stats(request):
    user_id = request.args.get("id")
    query = "SELECT count(*) FROM logs"
    cursor.execute(query)
    return cursor.fetchone()
