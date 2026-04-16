from flask import request
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def get_record(request):
    name = request.args.get("name")
    condition = "name = '" + name + "'"
    query = "SELECT * FROM records WHERE " + condition
    cursor.execute(query)
    return cursor.fetchall()
