import csv
import os
import re
import sqlite3
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import pandas as pd
 
# Imports for Google Colab auto-download
from google.colab import files

BASE_URL = "https://books.toscrape.com/catalogue/page-{}.html"

RATING_MAP = {
    "One": 1,
    "Two": 2,
    "Three": 3,
    "Four": 4,
    "Five": 5
}

books_data = []

print("Scraping pages 1 to 5...")

for page in range(1, 6):
    url = BASE_URL.format(page)
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article", class_="product_pod")

    for article in articles:
        # Title
        title = article.h3.a["title"]

        # Absolute URL
        relative_url = article.h3.a["href"]
        full_url = urljoin(url, relative_url)

        # Price as a float number
        price_text = article.find("p", class_="price_color").text
        price = float(re.sub(r"[^\d.]", "", price_text))

        # Rating as 1-5 integer
        rating_tag = article.find("p", class_="star-rating")
        rating_classes = rating_tag.get("class", [])
        rating_word = [c for c in rating_classes if c != "star-rating"][0]
        rating = RATING_MAP.get(rating_word, 0)

        # Availability as boolean
        availability_text = article.find("p", class_="instock availability").text.strip().lower()
        in_stock = "in stock" in availability_text

        books_data.append({
            "title": title,
            "price": price,
            "rating": rating,
            "in_stock": in_stock,
            "url": full_url
        })

print(f"Scraped {len(books_data)} books successfully!")

# ==========================================
# 1. SAVE TO CSV FILE
# ==========================================
csv_filename = "books.csv"
with open(csv_filename, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["title", "price", "rating", "in_stock", "url"])
    writer.writeheader()
    writer.writerows(books_data)

# ==========================================
# 2. SAVE TO SQLITE DATABASE FILE (.db)
# ==========================================
db_filename = "books.db"

# Convert to DataFrame to enforce schema and prevent JSON/Text format issues
df = pd.DataFrame(books_data)
df['price'] = df['price'].astype(float)
df['rating'] = df['rating'].astype(int)
df['in_stock'] = df['in_stock'].astype(bool)

# Create and persist the table into the SQLite database file
conn = sqlite3.connect(db_filename)
df.to_sql("books", conn, if_exists="replace", index=False)
conn.close()
 
print("Files saved successfully!")

# Display a quick preview in Colab
display(df.head())

# ==========================================
# 3. AUTOMATICALLY DOWNLOAD BOTH FILES
# ==========================================
print("Downloading books.csv and books.db to your device...")
files.download(csv_filename)
files.download(db_filename)
