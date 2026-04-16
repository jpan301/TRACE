from flask import request
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def build_query(user_id):
    return "SELECT * FROM users WHERE id = " + user_id

def get_user(request):
    user_id = request.args.get("id")
    query = build_query(user_id)
    cursor.execute(query)
    return cursor.fetchone()
