from flask import request
from sqlalchemy import create_engine, text
engine = create_engine("postgresql://localhost/test")

def search(request):
    term = request.args.get("q")
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT * FROM posts WHERE title = '{term}'"))
    return result.fetchall()
