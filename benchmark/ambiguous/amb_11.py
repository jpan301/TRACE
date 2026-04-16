# VULNERABLE: multi-step chain through helper that looks safe by name
# get_safe_query sounds like it produces a safe query but it does not
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def get_safe_query(user_input):
    # name is misleading — this just formats the string, no sanitization
    return "SELECT * FROM users WHERE name = '" + user_input + "'"

def search(name):
    query = get_safe_query(name)
    cursor.execute(query)
    return cursor.fetchall()
