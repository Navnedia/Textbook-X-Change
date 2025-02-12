from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .forms import ListingForm

def listings(request):
    return render(request, "listings.html", {"count": range(12)})

# Create your views here.
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)    
        if form.is_valid():
            form.save()
            return HttpResponse("Listing created successfully")
        else:
            print(form.errors)
            return render(request, "create_listing.html", {"form": form})

    else:
        form = ListingForm()
        return render(request, "create_listing.html", {"form":form})
#############################################################################################################################################

import numpy as np
import csv, os, re
from django.shortcuts import render
from django.views import View
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

CSV_FILE_PATH = "ebay_prices.csv"

# class EbayPriceScraperView(View):
#     def get(self, request):
#         return render(request, "landing.html")  
class EbayPriceScraperView(View):
    def get(self, request):
        isbn = request.GET.get("isbn")
        if not isbn:
            return JsonResponse({"error": "Missing ISBN"}, status=400)

        # Simulating API response for debugging
        return JsonResponse({"suggested_price": 25.99})  

    def post(self, request):
        isbn = request.POST.get("isbn", "").strip()
        if is_valid_isbn10(isbn)==False:
            return render(request, "landing.html", {"error": "Please enter a valid ISBN."})

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
                    elif "pre-owned" in condition_text:
                        prices_used.append(price)
                except Exception:
                    continue  

            driver.quit()

             # Remove outliers from new and used prices
            prices_new_filtered = prices_new 
            #prices_new_filtered = remove_outliers(prices_new)
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


            return render(request, "landing.html", {
                "isbn": isbn,
                "listings_found": len(prices_new) + len(prices_used),
                "new": {
                    "median_price": median_price_new,
                    "q1_price": q1_price_new,
                    "q3_price": q3_price_new,
                    "count": len(prices_new),
                    "price_samples": prices_new_filtered[:5]
                },
                "used": {
                    "median_price": median_price_used,
                    "q1_price": q1_price_used,
                    "q3_price": q3_price_used,
                    "suggested_list_price": suggested_list_price_used,
                    "suggested_buy_price": suggested_buy_price_used,
                    "count": len(prices_used),
                    "price_samples": prices_used_filtered[:5]
                }
            })

        except Exception as e:
            driver.quit()
            return render(request, "landing.html", {"error": str(e)})
        
def calculate_suggested_prices(prices):
    if not prices:
        return None, None 

    q1 = np.percentile(prices, 25)
    q3 = np.percentile(prices, 75)
    median = np.median(prices)
    min_price = min(prices)
    max_price = max(prices)
    price_spread = max_price - min_price

    # Suggested List (Sell) Price = median
    suggested_list_price = median

    # Suggested Buy Price - Q1 + Demand Factor
    suggested_buy_price = round(q1 + (0.1 * price_spread), 2)

    return suggested_list_price, suggested_buy_price

def remove_outliers(prices):
    """Remove outliers using the IQR method."""
    if len(prices) < 4:  # Not enough data for outlier removal
        return prices

    q1 = np.percentile(prices, 25)
    q3 = np.percentile(prices, 75)
    iqr = q3 - q1  # Interquartile Range
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    return [price for price in prices if lower_bound <= price <= upper_bound]

def save_to_csv(isbn, median_price_new, q1_price_new, q3_price_new, median_price_used, q1_price_used, 
                q3_price_used, suggested_list_price_used, suggested_buy_price_used):
    """Save search results to a CSV file."""
    file_exists = os.path.isfile(CSV_FILE_PATH)

    with open(CSV_FILE_PATH, mode="a", newline="") as file:
        writer = csv.writer(file)
        
        # If the file doesn't exist, write headers first
        if not file_exists:
            writer.writerow([
                "ISBN", 
                "Avg New Price", "Q1 New", "Q3 New", 
                "Avg Used Price", "Q1 Used", "Q3 Used", 
                "Suggested List Price (Used)", "Suggested Buy Price (Used)"
            ])
        
        # Write the search result
        writer.writerow([
            isbn, 
            median_price_new, q1_price_new, q3_price_new, 
            median_price_used, q1_price_used, q3_price_used, 
            suggested_list_price_used, suggested_buy_price_used
        ])



def is_valid_isbn10(isbn):
    # Remove dashes
    cleaned_isbn = isbn.replace("-", "")
    # Check if it contains exactly 10 digits


    # ISBN-10: 9 digits followed by a digit or 'X'
    isbn10_pattern = r"^\d{9}[\dX]$"
    # ISBN-13: Exactly 13 digits
    isbn13_pattern = r"^\d{13}$"

    if re.fullmatch(isbn10_pattern, cleaned_isbn):
        return True
    elif re.fullmatch(isbn13_pattern, cleaned_isbn):
        return True
    else:
        return False

