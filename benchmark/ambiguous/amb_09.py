# VULNERABLE: whitelist check is bypassable — checks prefix not full value
# looks like it has validation but the check is incomplete
# LLM should recognize the prefix check can be bypassed with table_name + "' OR 1=1--"
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def get_table_data(table_name):
    if not table_name.startswith("public_"):
        raise ValueError("only public tables allowed")
    # this check is bypassable: "public_users' OR 1=1--" passes the check
    query = f"SELECT * FROM {table_name}"
    cursor.execute(query)
    return cursor.fetchall()
