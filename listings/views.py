from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from .forms import ListingForm, PrelistForm
from .models import Listing
from .services.autofill import PrelistSuggestionsProvider

# Prelist View
def prelist(request: HttpRequest) -> HttpResponse:
    if request.POST:
        form = PrelistForm(request.POST)
        if form.is_valid():
            provider = PrelistSuggestionsProvider()
            listing = provider.process_data(isbn=form.cleaned_data["isbn"])
            
            return create_listing(request, autofill_data=listing)

    return render(request, "prelist.html", {"form": PrelistForm()})

# Create Listing View
def create_listing(request: HttpRequest, autofill_data: Listing | None = None) -> HttpResponse:
    if not autofill_data and request.method == "POST":
        form = ListingForm(request.POST, request.FILES)    
        if form.is_valid():
            form.save()
            return redirect("listings:listing_page") 
        else:
            print(form.errors)

    else:
        form = ListingForm(instance=autofill_data)
    return render(request, "create_listing.html", {"form": form})

# Listing Page with Filtering
def listing_page(request):
    location_filter = request.GET.get("location", "All")

    if location_filter == "Global":
        listings = Listing.objects.filter(location="Global").order_by("-id")
    elif location_filter == "Local":
        listings = Listing.objects.filter(location="Local").order_by("-id")
    else:
        listings = Listing.objects.all().order_by("-id")  # Default: Show all listings

    return render(request, "listings.html", {
        "listings": listings,
        "location_filter": location_filter
    })

# Textbook Details View
def textbook_details(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, "textbook_details.html", {"listing": listing})

############################################################################################################################
# Refactored code using AI for enhanced readability and maintainability

import re
import os
import csv
import numpy as np

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

# Selenium and other imports...
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Define CSV file path
CSV_FILE_PATH = "scraped_results.csv"

def calculate_suggested_prices(prices):
    if not prices:
        return None, None 
    q1 = np.percentile(prices, 25)
    q3 = np.percentile(prices, 75)
    median = np.median(prices)
    price_spread = max(prices) - min(prices)
    suggested_list_price = median  # Example: Use the median
    suggested_buy_price = round(q1 + (0.1 * price_spread), 2)
    return suggested_list_price, suggested_buy_price

def remove_outliers(prices):
    """Remove outliers using the IQR method."""
    if len(prices) < 4:
        return prices
    q1 = np.percentile(prices, 25)
    q3 = np.percentile(prices, 75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    return [price for price in prices if lower_bound <= price <= upper_bound]

def save_to_csv(isbn, median_price_new, q1_price_new, q3_price_new,
                median_price_used, q1_price_used, q3_price_used,
                suggested_list_price_used, suggested_buy_price_used):
    """Save search results to a CSV file."""
    file_exists = os.path.isfile(CSV_FILE_PATH)
    with open(CSV_FILE_PATH, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow([
                "ISBN", 
                "Avg New Price", "Q1 New", "Q3 New", 
                "Avg Used Price", "Q1 Used", "Q3 Used", 
                "Suggested List Price (Used)", "Suggested Buy Price (Used)"
            ])
        writer.writerow([
            isbn, 
            median_price_new, q1_price_new, q3_price_new, 
            median_price_used, q1_price_used, q3_price_used, 
            suggested_list_price_used, suggested_buy_price_used
        ])

def is_valid_isbn10(isbn):
    cleaned_isbn = isbn.replace("-", "")
    isbn10_pattern = r"^\d{9}[\dX]$"
    isbn13_pattern = r"^\d{13}$"
    return bool(re.fullmatch(isbn10_pattern, cleaned_isbn) or re.fullmatch(isbn13_pattern, cleaned_isbn))

class EbayPriceScraperView(View):
    def scrape_data(self, isbn):
        """Helper method that performs scraping and returns a dictionary of results."""
        # Setup Selenium WebDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            ebay_url = f"https://www.ebay.com/sch/i.html?_nkw={isbn}+textbook"
            driver.get(ebay_url)
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "s-item__price")))

            prices_new = []
            prices_used = []
            listings = driver.find_elements(By.CLASS_NAME, "s-item")

            for listing in listings:
                try:
                    price_element = listing.find_element(By.CLASS_NAME, "s-item__price")
                    price_text = price_element.text.replace("$", "").replace(",", "").strip()
                    price = float(price_text)
                    condition_element = listing.find_element(By.CLASS_NAME, "SECONDARY_INFO")
                    condition_text = condition_element.text.lower()

                    if "new" in condition_text:
                        prices_new.append(price)
                    elif "pre-owned" in condition_text or "used" in condition_text:
                        prices_used.append(price)
                except Exception:
                    continue  

            driver.quit()

            # Remove outliers from new and used prices
            prices_new_filtered = prices_new
            prices_used_filtered = remove_outliers(prices_used)

            # Compute price statistics for new books
            median_price_new = round(np.median(prices_new_filtered), 2) if prices_new_filtered else None
            q1_price_new = round(np.percentile(prices_new_filtered, 25), 2) if prices_new_filtered else None
            q3_price_new = round(np.percentile(prices_new_filtered, 75), 2) if prices_new_filtered else None

            # Compute price statistics for used books
            median_price_used = round(np.median(prices_used_filtered), 2) if prices_used_filtered else None
            q1_price_used = round(np.percentile(prices_used_filtered, 25), 2) if prices_used_filtered else None
            q3_price_used = round(np.percentile(prices_used_filtered, 75), 2) if prices_used_filtered else None

            # Calculate suggested prices for used books only
            suggested_list_price_used, suggested_buy_price_used = calculate_suggested_prices(prices_used_filtered)

            # Save results to CSV
            save_to_csv(
                isbn, median_price_new, q1_price_new, q3_price_new, 
                median_price_used, q1_price_used, q3_price_used, 
                suggested_list_price_used, suggested_buy_price_used
            )

            return {
                "isbn": isbn,
                "listings_found": len(prices_new) + len(prices_used),
                "new": {"median_price": median_price_new, "q1_price": q1_price_new, "q3_price": q3_price_new},
                "used": {"median_price": median_price_used, "q1_price": q1_price_used, "q3_price": q3_price_used}
            }
        except Exception as e:
            driver.quit()
            raise e

    def get(self, request):
        isbn = request.GET.get("isbn")
        if not isbn:
            return JsonResponse({"error": "Missing ISBN"}, status=400)
        if not is_valid_isbn10(isbn):
            return JsonResponse({"error": "Invalid ISBN"}, status=400)

        try:
            data = self.scrape_data(isbn)
            return JsonResponse(data)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
