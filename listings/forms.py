from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    class Meta:
        model=Listing
        fields=["title", "isbn", "author", "description", "price", "condition", "location","coursecode"]
        labels={
            "title":"Title",
            "isbn":"ISBN",
            "author":"Author",
            "description":"Description",
            "price":"Price",
            # "image":"Image",
            "condition":"Condition",
            "location":"location",
            "coursecode":"Course Code"
        }
        widgets={
            "title":forms.TextInput(attrs={"class":"form-control"}),
            "isbn":forms.TextInput(attrs={"class":"form-control"}),
            "author":forms.TextInput(attrs={"class":"form-control"}),
            "description":forms.Textarea(attrs={"class":"form-control"}),
            "price":forms.NumberInput(attrs={"class":"form-control"}),
            # "image":forms.ImageField(attrs={"class":"form-control"}),
            "condition":forms.Select(attrs={"class":"form-control"}),
            "location":forms.Select(attrs={"class":"form-control"}),
          "coursecode":forms.TextInput(attrs={"class":"form-control"})  
        }
