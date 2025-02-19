import requests
from listings.models import Listing


class PrelistSuggestionsProvider():

    API_URL = "https://openlibrary.org/api/books?bibkeys=ISBN:{}&jscmd=data&format=json"

    def data_request(self, isbn):
        try:
            response = requests.get(self.API_URL.format(isbn))
            response.raise_for_status()

            return response.json()
        except:
            print("request failed") # Add better handling in the future...

        return {}

    def process_data(self, isbn) -> Listing:
        isbn = isbn.replace('-', '')
        data = self.data_request(isbn)

        if data:
            data = data.get(f"ISBN:{isbn}")
            authors = data.get("authors", [])
            listing = Listing(
                isbn=isbn,
                title=data.get("title", None),
                author=authors[0]["name"] if authors else None 
            )
            return listing
        else:
            return Listing()


