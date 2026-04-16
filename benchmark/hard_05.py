# VULNERABLE: mixed safe and unsafe calls in same function
# one call is parameterized (safe), one is concatenated (vulnerable)
# tools need to flag only the unsafe one
from flask import request
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def get_data(request):
    user_id = request.args.get("id")
    search = request.args.get("q")

    # this one is safe
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()

    # this one is vulnerable
    query = "SELECT * FROM logs WHERE message LIKE '%" + search + "%'"
    cursor.execute(query)
    logs = cursor.fetchall()

    return user, logs
