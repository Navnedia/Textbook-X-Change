from django.shortcuts import render, get_object_or_404, redirect
from .models import WishList


# Create your views here.
def create_wish(request):
    return render(request, 'wishlist/createwish.html')


def request_book(request):
    if request.method == "POST":
        book_title = request.POST.get("book_title")
        author = request.POST.get("author")
        isbn = request.POST.get("isbn", "")

        # Save the request to the database
        if request.user.is_authenticated:
            WishList.objects.create(
                title=book_title,
                author=author,
                isbn=isbn,
                user=request.user  # Save the request for the logged-in user
            )

        return render(request, "wishlist/requestbook.html", {
            "success": True  # Display success message
        })

    return render(request, "wishlist/requestbook.html")

# View to display the user's requests
def my_requests(request):
    if request.user.is_authenticated:
        # Fetch requests made by the logged-in user
        user_requests = WishList.objects.filter(user=request.user)
    else:
        user_requests = []

    return render(request, "wishlist/myrequests.html", {"user_requests": user_requests})


# New view to handle editing a request
def edit_request(request, request_id):
    # Fetch the request by ID
    user_request = get_object_or_404(WishList, id=request_id, user=request.user)

    if request.method == "POST":
        user_request.title = request.POST.get("book_title")
        user_request.author = request.POST.get("author")
        user_request.isbn = request.POST.get("isbn", "")
        user_request.save()
        return redirect('wishlist:myRequests')  # Redirect to the "My Requests" page after saving changes

    return render(request, "wishlist/edit_request.html", {"request": user_request})

# New view to handle deleting a request
def delete_request(request, request_id):
    user_request = get_object_or_404(WishList, id=request_id, user=request.user)
    user_request.delete()
    return redirect('wishlist:myRequests')  # Redirect to "My Requests" page after deletion