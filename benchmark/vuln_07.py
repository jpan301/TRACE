from django.http import HttpRequest
import mysql.connector
conn = mysql.connector.connect(host="localhost", user="root", database="test")
cursor = conn.cursor()

def get_item(request):
    item_id = request.GET.get("item_id")
    query = "SELECT * FROM items WHERE id = %s" % item_id
    cursor.execute(query)
    return cursor.fetchone()
