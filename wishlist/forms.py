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

    # Aiden: For now, I want the ISBN reqired because it will make doing the fulfill autofill simpler.
    # Make ISBN optional
    # isbn = forms.CharField(required=False, strip=True, widget=forms.TextInput(attrs={'class': 'form-control text-center fw-bold'}))
