-- ============================================================
-- PART 2: SQL Analytics & Data Validation
-- Database: SQLite (books.db)
-- Target Table: books
-- ============================================================


-- ------------------------------------------------------------
-- Question 1: Average price for each rating
-- Calculates the mean price per star rating (rounded to 2 decimals)
-- ------------------------------------------------------------
SELECT 
    rating, 
    ROUND(AVG(price), 2) AS avg_price
FROM books
GROUP BY rating
ORDER BY rating ASC;


-- ------------------------------------------------------------
-- Question 2: The 5 most expensive books rated 4 or 5
-- Retrieves the top 5 highest priced books with ratings of 4 or 5 stars
-- ------------------------------------------------------------
SELECT 
    title, 
    price, 
    rating
FROM books
WHERE rating IN (4, 5)
ORDER BY price DESC
LIMIT 5;


-- ------------------------------------------------------------
-- Question 3: How many books are out of stock, per rating
-- Counts items where in_stock is False / 0
-- ------------------------------------------------------------
SELECT 
    rating, 
    COUNT(*) AS out_of_stock_count
FROM books
WHERE in_stock = 0 OR LOWER(CAST(in_stock AS TEXT)) = 'false'
GROUP BY rating
ORDER BY rating ASC;


-- ------------------------------------------------------------
-- Question 4 (Validation Query): Total count of in-stock books
-- Added for data validation to verify that 100% of scraped books are in stock
-- ------------------------------------------------------------
SELECT COUNT(*) AS total_in_stock
FROM books
WHERE in_stock = 1 OR LOWER(CAST(in_stock AS TEXT)) = 'true';