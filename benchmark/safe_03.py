import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def get_all_users():
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()
