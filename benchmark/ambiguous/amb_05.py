# SAFE: param controls logic flow, never enters the SQL string itself
# static engine flags because status param is in scope near execute
# LLM should see that status is used in Python if/else, not in query
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def get_records(status):
    if status == "active":
        query = "SELECT * FROM records WHERE active = 1"
    elif status == "archived":
        query = "SELECT * FROM records WHERE active = 0"
    else:
        query = "SELECT * FROM records"
    cursor.execute(query)   # query is always hardcoded, status never touches it
    return cursor.fetchall()
