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
# from django documentation

class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class FileFieldForm(forms.Form):
    file_field = MultipleFileField()

class ListingForm(forms.ModelForm):
    images = MultipleFileField(required=False)
    
    class Meta:
        model=Listing
        # fields=["title", "isbn", "author", "additional_details", "price", "condition", "location","coursecode"]
        fields=["additional_details", "price", "condition", "location"]
        # labels={
        #     "title":"Title",
        #     "isbn":"ISBN",
        #     "author":"Author",
        #     "additional_details":"Additional Details",
        #     "price":"Price",
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
        #     "condition":forms.Select(attrs={"class":"form-control"}),
        #     "location":forms.Select(attrs={"class":"form-control"}),
        #     "coursecode":forms.TextInput(attrs={"class":"form-control"})  
        # }
