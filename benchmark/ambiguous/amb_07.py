# SAFE: SQL is built only from a fixed enum — param controls choice not content
# static engine flags because order_by param flows near the query
# LLM should see the enum lookup prevents injection
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

ORDER_OPTIONS = {
    "name_asc": "ORDER BY name ASC",
    "name_desc": "ORDER BY name DESC",
    "date_asc": "ORDER BY created_at ASC",
    "date_desc": "ORDER BY created_at DESC",
}

def list_users(order_by):
    order_clause = ORDER_OPTIONS.get(order_by, "ORDER BY id ASC")
    query = "SELECT * FROM users " + order_clause   # order_clause is from fixed dict
    cursor.execute(query)
    return cursor.fetchall()
