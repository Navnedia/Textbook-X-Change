from django.shortcuts import render

# Create your views here.
def create_wish(request):
    return render(request, 'wishlist/createwish.html')


def request_book(request):
    if request.method == "POST":
        book_title = request.POST.get("book_title")
        author = request.POST.get("author")
        isbn = request.POST.get("isbn", "")

        # In a real app, you'd save this data to the database or send an email.

    return render(request, "wishlist/requestbook.html")