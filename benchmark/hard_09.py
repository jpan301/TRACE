# SAFE: user input used in application logic but never reaches SQL
# the SQL queries are all hardcoded
from flask import request
import psycopg2
conn = psycopg2.connect("dbname=test")
cursor = conn.cursor()

def get_report(request):
    report_type = request.args.get("type")  # user input
    start_date = request.args.get("start")  # user input

    # all queries are hardcoded — user input only used for Python logic
    cursor.execute("SELECT * FROM sales")
    sales = cursor.fetchall()

    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    # filter in Python based on user input, not in SQL
    if report_type == "sales":
        return [s for s in sales if str(s[2]) >= start_date]
    return [e for e in expenses if str(e[2]) >= start_date]
