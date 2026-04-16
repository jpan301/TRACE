# VULNERABLE: type check is bypassable via subclass or __int__ override
# looks safe because it checks type, but the check is not strict enough
# in practice this pattern is still dangerous
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def get_record(record_id):
    if not isinstance(record_id, (int, float)):   # float can still be injected via NaN
        raise TypeError("must be numeric")
    query = f"SELECT * FROM records WHERE id = {record_id}"
    cursor.execute(query)
    return cursor.fetchone()
