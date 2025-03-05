from django.shortcuts import render, get_object_or_404, redirect
from .models import WishList
from django.contrib.auth.decorators import login_required
from .forms import WishListForm


@login_required
def request_book(request):
    if request.method == "POST":
        form = WishListForm(request.POST)
        if form.is_valid():
            wish = form.save(commit=False)
            wish.user = request.user
            wish.save()
            return render(request, "wishlist/requestbook.html", {
                "success": True  # Display success message
            })
    else:
        form = WishListForm()

    return render(request, "wishlist/requestbook.html", {'form': form})

# View to display the user's requests
@login_required
def my_requests(request):
    # Fetch requests made by the logged-in user
    user_requests = WishList.objects.filter(user=request.user)

    return render(request, "wishlist/myrequests.html", {"user_requests": user_requests})


# New view to handle editing a request
@login_required
def edit_request(request, request_id):
    user_request = get_object_or_404(WishList, id=request_id, user=request.user)

    if request.method == "POST":
        form = WishListForm(request.POST, instance=user_request)
        if form.is_valid():
            form.save()
            return redirect('wishlist:myrequests')  # Redirect to "My Requests" page after saving changes
    else:
        form = WishListForm(instance=user_request)

    return render(request, "wishlist/edit_request.html", {"form": form, "request": user_request})


# New view to handle deleting a request
@login_required
def delete_request(request, request_id):
    user_request = get_object_or_404(WishList, id=request_id, user=request.user)
    user_request.delete()
    return redirect('wishlist:myrequests')  # Redirect to "My Requests" page after deletion


def all_requests(request):
    # Fetch all requests from the database
    requests = WishList.objects.all()
    return render(request, 'wishlist/browse_all_requests.html', {'requests': requests})
