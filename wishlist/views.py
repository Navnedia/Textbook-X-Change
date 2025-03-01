from django.shortcuts import render

# Create your views here.
def create_wish(request):
    return render(request, 'wishlist/create_wish.html')