from django.http import HttpRequest
from myapp.models import User

def get_user(request):
    user_id = request.GET.get("id")
    return User.objects.filter(id=user_id).first()
