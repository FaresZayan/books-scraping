# 📚 Books Scraping & SQL Analytics

An end-to-end data engineering mini-pipeline that scrapes book data from [Books to Scrape](https://books.toscrape.com/?utm_source=gemini), performs automated cleaning, exports structured datasets (CSV & SQLite), and executes analytical SQL queries for business insights.

---

## 📁 Project Structure

```text
.
├── book_scraping_task.py   # Python scraping pipeline & automated SQLite exporter
├── books.csv               # Exported dataset in CSV format (100 records)
├── Books.db                # SQLite database with structured types (float, int, bool)
├── queries.sql             # SQL analytics queries and data validation script
└── README.md               # Project documentation

```

---

## 🛠️ Part 1 — Web Scraping & Data Cleaning (`book_scraping_task.py`)

The extraction script parses pages **1 to 5** (100 books in total) using `requests` and `BeautifulSoup`.

### Data Cleaning & Transformation Pipeline:

* **Currency Removal:** Strip non-numeric currency symbols (`£`) using Regular Expressions (`re.sub(r"[^\d.]", "", price)`).
* **Rating Mapping:** Convert string ratings (`One` through `Five`) into explicit integers (`1` to `5`).
* **Schema Enforcement:** Convert extracted structures into Pandas DataFrames with strict type casting (`float` for price, `int` for rating, `bool` for stock status) before persistence.

---

## 📊 Part 2 — SQL Analytics (`queries.sql`)

Calculations executed on `Books.db` via SQLite:

### 1. Average Price per Rating

```sql
SELECT 
    rating, 
    ROUND(AVG(price), 2) AS avg_price
FROM books
GROUP BY rating
ORDER BY rating ASC;

```

| Rating | Average Price (£) |
| --- | --- |
| 1 | 35.52 |
| 2 | 35.91 |
| 3 | 36.84 |
| 4 | 33.98 |
| 5 | 30.01 |

---

### 2. Top 5 Most Expensive Books (Rated 4 or 5)

```sql
SELECT title, price, rating
FROM books
WHERE rating IN (4, 5)
ORDER BY price DESC
LIMIT 5;

```

| Title | Price (£) | Rating |
| --- | --- | --- |
| The Death of Humanity: and the Case for Life | 58.11 | 4 |
| The Past Never Ends | 56.50 | 4 |
| Sapiens: A Brief History of Humankind | 54.23 | 5 |
| Scott Pilgrim's Precious Little Life (Scott Pilgrim #1) | 52.29 | 5 |
| Behind Closed Doors | 52.22 | 4 |

---

### 3. Out of Stock Count per Rating

```sql
SELECT 
    rating, 
    COUNT(*) AS out_of_stock_count
FROM books
WHERE in_stock = 0 OR LOWER(CAST(in_stock AS TEXT)) = 'false'
GROUP BY rating
ORDER BY rating ASC;

```

*(Result: 0 records returned, as 100% of the scraped sample is currently in stock).*

---

### 4. Data Validation Query

```sql
SELECT COUNT(*) AS total_in_stock
FROM books
WHERE in_stock = 1 OR LOWER(CAST(in_stock AS TEXT)) = 'true';

```

*(Total in-stock items verified: **100**).*

---

## 💡 Part 3 — Technical Reflection

* **What broke, or took longer than expected?**
Automating currency symbol (`£`) stripping using regex directly inside the Python pipeline to enforce strict `float` typing in SQLite. This ensured SQL aggregate functions (`AVG()`, `ORDER BY DESC`) executed natively without manual spreadsheet intervention.
* **If the site started blocking after 50 requests, what would you change?**
* Introduce delay intervals using `time.sleep()`.
* Add custom request headers (`User-Agent` spoofing).
* Implement proxy server rotation.
* Upgrade to browser automation frameworks like `Playwright` or `Selenium` to handle potential dynamic JavaScript challenges.
  ## 📊 Power BI Dashboard

Here is an interactive preview of the executive dashboard built using Power BI Desktop:

![Power BI Dashboard](dashboard.png)

### Key Insights & KPIs Covered:
- **Total Books Scraped & Average Price**: Real-time aggregation of catalog metrics.
- **Price vs. Rating Analysis**: Visualizing pricing trends across rating tiers.
- **Stock Availability**: Monitoring inventory levels.
- **Top 5 Most Expensive Books**: Highlighting premium inventory.
