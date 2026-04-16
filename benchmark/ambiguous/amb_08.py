# VULNERABLE: sanitizer only strips spaces — does not prevent injection
# looks safe because there is a "sanitize" step before use
# LLM should recognize that stripping spaces is not SQL injection protection
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def weak_sanitize(value):
    return value.strip()   # strips whitespace only — totally insufficient

def get_user(username):
    safe_name = weak_sanitize(username)   # false sense of security
    query = "SELECT * FROM users WHERE name = '" + safe_name + "'"
    cursor.execute(query)
    return cursor.fetchone()
