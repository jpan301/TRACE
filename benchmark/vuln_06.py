from flask import request
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def get_record(request):
    table = request.args.get("table")
    col = request.args.get("col")
    val = request.args.get("val")
    base = "SELECT * FROM " + table
    condition = " WHERE " + col + " = '" + val + "'"
    query = base + condition
    cursor.execute(query)
    return cursor.fetchall()
