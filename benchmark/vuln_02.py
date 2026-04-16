from flask import request
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def search_user(request):
    name = request.args.get("name")
    cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")
    return cursor.fetchall()
