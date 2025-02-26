from django.urls import path
from .views import login_view, register_view, forgot_password_view, logout_view, custom_password_reset_confirm
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("forgot-password/", forgot_password_view, name="forgot_password"),
    path("logout/", logout_view, name="logout"),
    path("forgot_password/", auth_views.PasswordResetView.as_view(template_name="forgot_password.html"), name="forgot_password"),
    path("password_reset_email_sent/", auth_views.PasswordResetDoneView.as_view(template_name="password_reset_email_sent.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", custom_password_reset_confirm, name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="new_password_complete.html"), name="password_reset_complete"),
]