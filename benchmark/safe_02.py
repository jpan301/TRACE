from django.http import HttpRequest
import pymysql
conn = pymysql.connect(host="localhost", user="root", db="test")
cursor = conn.cursor()

def get_order(request):
    order_id = request.GET.get("order_id")
    cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
    return cursor.fetchone()
