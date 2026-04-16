# SAFE: multiple database calls, all parameterized
# looks complex but every call is safe
from django.http import HttpRequest
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def get_dashboard(request):
    user_id = request.GET.get("uid")
    search = request.GET.get("q")
    status = request.GET.get("status")

    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    cursor.execute("SELECT * FROM posts WHERE author_id = %s AND title LIKE %s",
                   (user_id, f"%{search}%"))
    posts = cursor.fetchall()

    cursor.execute("SELECT * FROM orders WHERE user_id = %s AND status = %s",
                   (user_id, status))
    orders = cursor.fetchall()

    return user, posts, orders
