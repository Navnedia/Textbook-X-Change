from django import forms
from django_select2 import forms as s2forms
from .models import School


class SchoolWidget(s2forms.ModelSelect2Widget):
    model = School
    search_fields=['name__icontains']