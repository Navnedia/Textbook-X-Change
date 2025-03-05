from django.urls import path
from .forms import LoginForm
from .views import custom_password_reset_confirm, RegistrationView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("", auth_views.LoginView.as_view(template_name="login.html", authentication_form=LoginForm), name="login"),
    path("register/", RegistrationView.as_view(), name="register"),
    path("logout/", auth_views.LogoutView.as_view(template_name="login.html"), name="logout"),
    path("password_reset/", auth_views.PasswordResetView.as_view(template_name="forgot_password.html"), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="password_reset_email_sent.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", custom_password_reset_confirm, name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="new_password_complete.html"), name="password_reset_complete"),
]