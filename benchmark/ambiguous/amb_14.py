# SAFE: uses ORM — no raw SQL at all
# static engine might flag because variable names look like SQL
# LLM should recognize Django ORM calls are not raw SQL execution
from django.contrib.auth.models import User

def get_user(user_id):
    # this is an ORM call — parameterized internally by Django
    # no raw SQL is constructed here
    return User.objects.filter(id=user_id).first()
