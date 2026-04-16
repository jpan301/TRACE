# SAFE: int() conversion makes injection impossible
# static engine flags it in broad mode because user_id is a param
# LLM should recognize int() as a sanitizer and suppress
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def get_user(user_id):
    try:
        user_id = int(user_id)   # converts to int — injection impossible
    except ValueError:
        return None
    query = "SELECT * FROM users WHERE id = " + str(user_id)
    cursor.execute(query)
    return cursor.fetchone()
