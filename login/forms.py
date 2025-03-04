from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _
from core.forms import SchoolWidget
from core.models import School
from .models import Profile


class UserRegistrationForm(UserCreationForm):
     email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={
            "autocomplete": "email", 
            "class": "form-control w-100 bg-light-subtle text-body-emphasis",
            "required": True,
            "placeholder": "Email"
        }),
     )

     school = forms.ModelChoiceField(
         queryset= School.objects.all(),
         widget=SchoolWidget(
            attrs={
                "required": True,
                #  "data-minimum-input-length": 0, # Default is 2 characters minimum.
                "class": "form-select form-select-lg",
                "data-placeholder": "Select your school"
            }
     ))

     def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "class": "form-control w-100 bg-light-subtle text-body-emphasis", 
            "placeholder": "Username"
        })
        self.fields["password1"].widget.attrs.update({
            "class": "form-control w-100 bg-light-subtle text-body-emphasis",
            "required": True,
            "placeholder": "Password"
        })
        self.fields["password2"].widget.attrs.update({
            "class": "form-control w-100 bg-light-subtle text-body-emphasis",
            "required": True,
            "placeholder": "Confirm Password"
        })

     def clean_email(self):
        email = self.cleaned_data['email']
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        
        return email
     
     # Override the save method so we can handle additional data processing.
     def save(self, commit=True):
         user = super().save(commit=False)
         user.email = self.cleaned_data["email"] # add the email manually.

         if commit:
            user.save()
            try:
                # The profile should be automatically created when the user is saved, we just need to populate the school:
                profile: Profile = user.profile
                profile.school = self.cleaned_data['school']
                profile.save()
            except ObjectDoesNotExist:
                print("Profile failed to create!")

         return user

# Extending Auth login from for custom field class styling:
class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({
            "class": "form-control w-100 bg-light-subtle text-body-emphasis", 
            "placeholder": "Username"
        })
        self.fields["password"].widget.attrs.update({
            "class": "form-control w-100 bg-light-subtle text-body-emphasis",
            "required": True,
            "placeholder": "Password"
        })