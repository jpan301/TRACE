from flask import request
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def get_product(request):
    pid = request.args.get("pid")
    query = "SELECT * FROM products WHERE id = '%s'" % pid
    cursor.execute(query)
    return cursor.fetchone()
