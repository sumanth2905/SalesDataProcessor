-- Table creation
CREATE TABLE public.SalesData (
    "OrderId" TEXT UNIQUE,
    "OrderItemId" BIGINT,
    "QuantityOrdered" BIGINT,
    "ItemPrice" DOUBLE PRECISION,
    "PromotionDiscount" JSONB, 
    "Region" TEXT,
    "TotalSales" DOUBLE PRECISION
);

-- Count the total number of records.
select count(*) from SalesData ;

-- Find the total sales amount by region. 
SELECT "Region", SUM("TotalSales") AS "TotalSalesPerRegion" 
FROM SalesData 
GROUP BY "Region";


-- Find the average sales amount per transaction. 
SELECT AVG("TotalSales") FROM SalesData;

-- Ensure there are no duplicate id values
-- Since unique constrain is already added we can check for duplicate entries to verify there are no duplicate id values
SELECT "OrderId", COUNT(*) AS "DuplicateCount"
FROM "salesdata"
GROUP BY "OrderId"
HAVING COUNT(*) > 1;

