from django.shortcuts import redirect
from django.contrib import messages
from AdminApp.views import *

def admin_required(view_func):
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            messages.error(request, "Please login as admin.")
            return redirect(admin_login)

        if request.user.role != "admin" and not request.user.is_superuser:
            messages.error(request, "You are not authorized to access admin panel.")
            return redirect("home")

        return view_func(request, *args, **kwargs)

    return wrapper