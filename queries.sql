-- ================================================
-- Cloud Kitchen Market Intelligence Project
-- Name: Richa Dhiman
-- Date: June 3, 2026
-- Locality: Gangapur Road, Nashik
-- ================================================


-- ================================================
-- SECTION 1: DATABASE SCHEMA
-- ================================================

-- Table 1: Restaurants
CREATE TABLE restaurants (
    id              INT PRIMARY KEY AUTO_INCREMENT,
    name            VARCHAR(150) NOT NULL,
    cuisine         VARCHAR(300),
    dining_rating   VARCHAR(10),
    delivery_rating VARCHAR(10),
    reviews         INT,
    cost_for_two    INT,
    locality        VARCHAR(100),
    address         VARCHAR(300),
    delivery_time   VARCHAR(50),
    type            VARCHAR(50)
);

-- Table 2: Menu Items
CREATE TABLE menu_items (
    id              INT PRIMARY KEY AUTO_INCREMENT,
    restaurant_id   INT NOT NULL,
    restaurant_name VARCHAR(150),
    category        VARCHAR(100),
    item_name       VARCHAR(200),
    price           INT,
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
);


-- ================================================
-- SECTION 2: SQL QUERIES
-- ================================================

-- Query 1: Top 5 highest rated restaurants (by dining rating)
-- Excludes 'New' ratings and NULL values
SELECT 
    name,
    cuisine,
    dining_rating,
    reviews,
    cost_for_two
FROM restaurants
WHERE dining_rating NOT IN ('New', 'NA')
  AND dining_rating IS NOT NULL
ORDER BY CAST(dining_rating AS DECIMAL(3,1)) DESC
LIMIT 5;


-- Query 2: Average cost-for-two by cuisine
-- Note: Since one restaurant can have multiple cuisines,
-- this query treats each restaurant's primary cuisine separately
SELECT 
    cuisine,
    ROUND(AVG(cost_for_two), 2) AS average_cost_for_two,
    COUNT(*) AS number_of_restaurants
FROM restaurants
WHERE cost_for_two IS NOT NULL
GROUP BY cuisine
ORDER BY average_cost_for_two DESC;


-- Query 3: Restaurants with more than one cuisine tag
-- Identifies restaurants offering multiple cuisines (comma separated)
SELECT 
    name,
    cuisine,
    type,
    locality,
    (LENGTH(cuisine) - LENGTH(REPLACE(cuisine, ',', '')) + 1) AS cuisine_count
FROM restaurants
WHERE cuisine LIKE '%,%'
ORDER BY cuisine_count DESC;


-- Query 4: Highest priced menu item across all restaurants
SELECT 
    m.restaurant_name,
    m.category,
    m.item_name,
    m.price
FROM menu_items m
WHERE m.price = (
    SELECT MAX(price) 
    FROM menu_items
);


-- BONUS Query 5: Restaurants with highest number of reviews
SELECT
    name,
    reviews,
    dining_rating,
    type
FROM restaurants
WHERE reviews IS NOT NULL
ORDER BY reviews DESC
LIMIT 5;


-- BONUS Query 6: Count of restaurants by type
SELECT
    type,
    COUNT(*) AS total_restaurants
FROM restaurants
GROUP BY type
ORDER BY total_restaurants DESC;