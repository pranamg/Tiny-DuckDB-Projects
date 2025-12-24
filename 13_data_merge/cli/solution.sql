-- Chapter 13: Data Merge - Solution
-- Merge player profiles using DuckDB 1.4's MERGE statement

-- Create target table (existing players)
CREATE OR REPLACE TABLE players (
    player_id INTEGER PRIMARY KEY,
    username VARCHAR,
    score INTEGER,
    last_login DATE,
    status VARCHAR DEFAULT 'active'
);

INSERT INTO players VALUES
    (1, 'Alice', 1500, '2024-01-15', 'active'),
    (2, 'Bob', 1200, '2024-01-10', 'active'),
    (3, 'Charlie', 800, '2023-12-01', 'inactive');

-- Create source table (updates)
CREATE OR REPLACE TEMP TABLE player_updates (
    player_id INTEGER,
    username VARCHAR,
    score INTEGER,
    last_login DATE,
    status VARCHAR
);

INSERT INTO player_updates VALUES
    (1, 'Alice', 1800, '2024-01-20', 'active'),     -- Update existing
    (2, 'Bob', 1200, '2024-01-10', 'deleted'),       -- Mark for deletion
    (4, 'Diana', 2000, '2024-01-19', 'active');      -- New player

-- Perform the merge
MERGE INTO players AS target
USING player_updates AS source
ON target.player_id = source.player_id
WHEN MATCHED AND source.status = 'deleted' THEN
    DELETE
WHEN MATCHED THEN
    UPDATE SET 
        score = source.score,
        last_login = source.last_login,
        status = source.status
WHEN NOT MATCHED THEN
    INSERT (player_id, username, score, last_login, status)
    VALUES (source.player_id, source.username, source.score, source.last_login, source.status);

-- Show results
SELECT * FROM players ORDER BY player_id;
