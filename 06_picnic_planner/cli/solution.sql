-- Chapter 06: Picnic Planner - Solution
-- Format item lists with proper grammar

WITH items AS (
    SELECT unnest(['chips', 'dip', 'salsa', 'guacamole']) as item
),
item_list AS (
    SELECT list(item) as all_items FROM items
)
SELECT 
    CASE 
        WHEN len(all_items) = 1 THEN all_items[1]
        WHEN len(all_items) = 2 THEN all_items[1] || ' and ' || all_items[2]
        ELSE array_to_string(all_items[1:-1], ', ') || ', and ' || all_items[-1]
    END as formatted_list
FROM item_list;
