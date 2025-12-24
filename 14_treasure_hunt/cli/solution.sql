-- Chapter 14: Treasure Hunt - Solution
-- Find treasure locations using spatial extension

-- Install and load spatial extension
INSTALL spatial;
LOAD spatial;

-- Create treasure locations
CREATE OR REPLACE TABLE treasures (
    id INTEGER,
    name VARCHAR,
    location GEOMETRY,
    value INTEGER
);

INSERT INTO treasures VALUES
    (1, 'Golden Chest', ST_Point(10.5, 20.3), 1000),
    (2, 'Silver Coins', ST_Point(15.2, 18.7), 500),
    (3, 'Ancient Artifact', ST_Point(8.1, 25.4), 2500),
    (4, 'Gem Pouch', ST_Point(12.0, 22.0), 750),
    (5, 'Pirate Map', ST_Point(50.0, 50.0), 100);

-- Player position
CREATE OR REPLACE TEMP TABLE player AS
SELECT ST_Point(10.0, 20.0) as location;

-- Find treasures within radius of 10 units
SELECT 
    t.name,
    t.value,
    ROUND(ST_Distance(t.location, p.location)::NUMERIC, 2) as distance,
    ST_AsText(t.location) as coordinates
FROM treasures t, player p
WHERE ST_DWithin(t.location, p.location, 10.0)
ORDER BY distance;
