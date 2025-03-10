from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from login.forms import UserRegistrationForm


class RegistrationView(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = "register.html"
    success_url = "/login/"
    success_message = "Account created successfully! You can now log in."

    def get(self, request, *args, **kwargs):
        next = request.GET.get("next", None)
        if next:
            self.extra_context = { "next": next }
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        next = request.POST.get("next", None)
        if next:
            self.success_url = f"{self.success_url}?next={next}"
        return super().post(request, *args, **kwargs)


def custom_password_reset_confirm(request, uidb64, token):
    """Handles password reset confirmation and redirects to login on success."""
    view = PasswordResetConfirmView.as_view(
        template_name="create_new_password.html"
    )
    
    response = view(request, uidb64=uidb64, token=token)

    # If the form submission was successful, explicitly redirect to login
    if request.method == "POST" and response.status_code == 200:
        return HttpResponseRedirect(reverse("login"))

    return response