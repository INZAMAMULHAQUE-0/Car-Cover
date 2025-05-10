import requests
from bs4 import BeautifulSoup
import csv

# OLX search URL for 'car cover'
URL = "https://www.olx.in/items/q-car-cover"

# Custom headers to simulate a browser
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def fetch_olx_listings(url):
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")
    
    listings = []

    for item in soup.select("li.EIR5N"):
        title = item.select_one("span._2tW1I")
        price = item.select_one("span._89yzn")
        location = item.select_one("span._2tW1I._2xKfz")
        
        if title and price:
            listings.append({
                "Title": title.text.strip(),
                "Price": price.text.strip(),
                "Location": location.text.strip() if location else "N/A"
            })

    return listings

def save_to_csv(data, filename="olx_car_covers.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Title", "Price", "Location"])
        writer.writeheader()
        for item in data:
            writer.writerow(item)

if _name_ == "_main_":
    print("Fetching listings from OLX...")
    data = fetch_olx_listings(URL)
    save_to_csv(data)
    print(f"Saved {len(data)} listings to 'olx_car_covers.csv'")