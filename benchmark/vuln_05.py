from django.http import HttpRequest
import pymysql
conn = pymysql.connect(host="localhost", user="root", db="test")
cursor = conn.cursor()

def search_product(request):
    keyword = request.POST.get("keyword")
    cursor.execute(f"SELECT * FROM products WHERE name LIKE '%{keyword}%'")
    return cursor.fetchall()
