from flask import request
from sqlalchemy import create_engine, text
engine = create_engine("postgresql://localhost/test")

def search(request):
    term = request.args.get("q")
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT * FROM posts WHERE title = :term"),
            {"term": term}
        )
    return result.fetchall()
