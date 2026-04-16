from flask import request
import mysql.connector
conn = mysql.connector.connect(host="localhost", user="root", database="test")
cursor = conn.cursor()

def get_item(request):
    item_id = request.args.get("item_id")
    cursor.execute("SELECT * FROM items WHERE id = %s", (item_id,))
    return cursor.fetchone()
