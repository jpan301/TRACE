# SAFE: parameterized query — second arg to execute is a tuple
# static engine might be confused by the f-string building the base query
# LLM should recognize the %s placeholder with tuple argument is safe
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def get_user(user_id, schema):
    # the schema part looks dangerous but user_id is parameterized
    query = f"SELECT * FROM {schema}.users WHERE id = %s"
    cursor.execute(query, (user_id,))   # user_id is safely parameterized
    return cursor.fetchone()
