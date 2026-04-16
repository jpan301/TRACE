from django.http import HttpRequest
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def update_email(request):
    user_id = request.POST.get("user_id")
    email = request.POST.get("email")
    query = "UPDATE users SET email = '" + email + "' WHERE id = " + user_id
    cursor.execute(query)
    conn.commit()
