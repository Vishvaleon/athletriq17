from django.urls import path
from .views import signup_view, login_view, logout_view, admin_dashboard

urlpatterns = [
    path("signup/", signup_view, name="signup"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),  
    path("admin-dashboard/", admin_dashboard, name="admin_dashboard"),
]
