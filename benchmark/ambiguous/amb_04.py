# SAFE: isinstance check guarantees the value is an integer
# static engine flags because row_id is a param that enters the query
# LLM should recognize isinstance(x, int) as type safety
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def fetch_row(row_id):
    if not isinstance(row_id, int):
        raise TypeError("row_id must be an integer")
    query = "SELECT * FROM records WHERE id = " + str(row_id)
    cursor.execute(query)
    return cursor.fetchone()
