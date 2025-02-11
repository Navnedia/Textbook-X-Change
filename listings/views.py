from django.shortcuts import render
from django.http import HttpResponse
from .forms import ListingForm

# Create your views here.
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)    
        if form.is_valid():
            form.save()
            return HttpResponse("Listing created successfully")
        else:
            print(form.errors)
            return HttpResponse("Invalid form")
    else:
        form = ListingForm()
        return render(request, "create_listing.html", {"form":form})
