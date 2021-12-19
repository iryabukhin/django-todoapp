from django.contrib import auth
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.shortcuts import render, redirect


def redirect_back(request):
    return redirect(request.META.get("HTTP_REFERER"))


class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(request, username=username, password=password)

        if not user:
            messages.error(request, "Login failed. Please try again.")
            return redirect_back(request)

        auth.login(request, user)
        messages.success(request, "You are now logged in as {}.".format(username))

        return redirect("index")


class LogoutView(View, LoginRequiredMixin):

    login_url = "/login"
    redirect_field_name = "redirect_to"

    def get(self, request):
        auth.logout(request)
        return redirect("login")


def signup_submit(req):
    email = req.POST.get("email")
    username = req.POST.get("username")
    password1 = req.POST.get("password1")
    password2 = req.POST.get("password2")

    if User.objects.filter(username=username).exists():
        messages.error(req, "Username '{}' is already taken.".format(username))
        return redirect_back(req)

    if User.objects.filter(email=email).exists():
        messages.error(req, "Email {} is already taken.".format(email))
        return redirect_back(req)

    if password1 != password2:
        messages.error(req, "Password confirmation is incorrect!")
        return redirect_back(req)

    try:
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1
        )
    except Exception as e:
        user = None

    if not user:
        messages.error(req, "Error creating a new user.")
        return redirect_back(req)

    messages.success(req, "Created user")
    auth.login(req, user)
    return redirect("index")
