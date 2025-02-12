from django.urls import path
from .views import login_view, register_view, forgot_password_view, logout_view

urlpatterns = [
    path("", login_view, name="login"),  # The login page is at "login/"
    path("register/", register_view, name="register"),
    path("forgot-password/", forgot_password_view, name="forgot_password"),
    path("logout/", logout_view, name="logout"),
]