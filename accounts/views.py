from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import CustomUser
from django.contrib import messages
from mainapp.models import Athlete, Certificate

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            if user.username == "admin":  # ✅ Admin Login
                return redirect("admin_dashboard")

            elif user.username == "zeo":  # ✅ If 'zeo' logs in
                return redirect("athlete_dashboard")  

            else:  # ✅ Any other user
                return redirect("role_selection")  

        else:
            messages.error(request, "Invalid username or password")
    return render(request, "registration/login.html")

def signup_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # ✅ Check if username already exists
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Choose a different one.")
            return redirect("signup")

        # ✅ Create new user
        user = CustomUser.objects.create_user(username=username, password=password)
        user.save()
        
        messages.success(request, "Account created successfully! Please log in.")
        return redirect("login")  # Redirect to login page after successful signup

    return render(request, "registration/signup.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("login")  # ✅ Redirect to Login Page


def custom_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            print(f"User {user.username} is_superuser: {user.is_superuser}")  # ✅ Debugging

            if user.is_superuser:
                print("Redirecting to admin dashboard...")
                return redirect("admin_dashboard")  # ✅ Redirect admin

            print("Redirecting to role selection...")
            return redirect("role_selection")  # ✅ Redirect normal users
        
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "login.html")


def is_admin(user):
    return user.is_superuser  # ✅ Allow only admins

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    athletes = Athlete.objects.all()
    certificates = Certificate.objects.all()

    return render(request, "admin_dashboard.html", {
        "athletes": athletes,
        "certificates": certificates
    })