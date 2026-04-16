# SAFE: regex validates that input is numeric before use
# static engine flags because user_id flows from param into query
# LLM should recognize the regex validation as protection
import re
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def get_user(user_id):
    if not re.match(r'^\d+$', str(user_id)):
        raise ValueError("user_id must be numeric")
    query = "SELECT * FROM users WHERE id = " + user_id
    cursor.execute(query)
    return cursor.fetchone()
