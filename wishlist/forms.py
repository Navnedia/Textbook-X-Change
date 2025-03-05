#Use django forms
from django import forms
from .models import WishList

class WishListForm(forms.ModelForm):
    class Meta:
        model = WishList
        fields = ['title', 'author', 'isbn']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control text-center fw-bold'}),
            'author': forms.TextInput(attrs={'class': 'form-control text-center fw-bold'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control text-center fw-bold'}),
        }
