from django import forms
from .models import Listing


LOCATION_FILTER_CHOICES = {
    "All": "All",
    "Local": "Local",
    "Global": "Global"
}

class SearchForm(forms.Form):
    # Search query visually hidden but included so that filters narrow down the existing search:
    q = forms.CharField(
        required=False,
        strip=True,
        widget=forms.HiddenInput()
    )

    location = forms.ChoiceField(
        required=False,
        choices=LOCATION_FILTER_CHOICES,
        widget=forms.RadioSelect(attrs={"class": "form-check-input"}),
    )



class PrelistForm(forms.Form):
    # For now, the form will only accept an ISBN number, but we might allow 
    # it to accept details like the title or author in the future.
    isbn = forms.CharField(
        max_length=14,
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter the ISBN'}
        )
    )


class ListingForm(forms.ModelForm):
    class Meta:
        model=Listing
        fields=["additional_details", "price", "condition", "location", "image"]
        # labels={
        #     "title":"Title",
        #     "isbn":"ISBN",
        #     "author":"Author",
        #     "additional_details":"Additional Details",
        #     "price":"Price",
        #     "image":"Upload Image",
        #     "condition":"Condition",
        #     "location":"location",
        #     "coursecode":"Course Code"
        # }
        # widgets={
        #     "title":forms.TextInput(attrs={"class":"form-control"}),
        #     "isbn":forms.TextInput(attrs={"class":"form-control"}),
        #     "author":forms.TextInput(attrs={"class":"form-control"}),
        #     "additional_details":forms.Textarea(attrs={"class":"form-control"}),
        #     "price":forms.NumberInput(attrs={"class":"form-control"}),
        #     "image": forms.ClearableFileInput(attrs={"class": "form-control"}), 
        #     "condition":forms.Select(attrs={"class":"form-control"}),
        #     "location":forms.Select(attrs={"class":"form-control"}),
        #   "coursecode":forms.TextInput(attrs={"class":"form-control"})  
        # }
