# VULNERABLE: validation only covers one of two user inputs
# looks like it validates but only name is checked, not order_field
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def search_users(name, order_field):
    if not name.isalpha():
        raise ValueError("name must be alphabetic")
    # name is validated but order_field is not — still injectable
    query = f"SELECT * FROM users WHERE name = '{name}' ORDER BY {order_field}"
    cursor.execute(query)
    return cursor.fetchall()
