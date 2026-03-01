from django.shortcuts import redirect
from django.contrib import messages
from UserApp.views import *
from AdminApp.models import User

def owner_required(view_func):
    def wrapper(request, *args, **kwargs):

        username = request.session.get('username')

        if not username:
            messages.error(request, "Please login first.")
            return redirect("user_signup")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User not found.")
            return redirect("user_signup")

        if user.role != "owner":
            messages.error(request, "You are not authorized to access this page.")
            return redirect("home")

        return view_func(request, *args, **kwargs)

    return wrapper