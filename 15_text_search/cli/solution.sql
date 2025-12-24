-- Chapter 15: Text Search - Solution
-- Search game dialogue using full-text search

-- Install and load FTS extension
INSTALL fts;
LOAD fts;

-- Load dialogue data
CREATE OR REPLACE TABLE dialogue AS
SELECT * FROM read_csv('../inputs/game_dialogue.csv');

-- Create FTS index on the dialogue column
PRAGMA create_fts_index('dialogue', 'id', 'dialogue');

-- Search for dialogue containing "crystal"
SELECT 
    id,
    speaker,
    location,
    dialogue,
    fts_main_dialogue.match_bm25(id, 'crystal') as score
FROM dialogue
WHERE fts_main_dialogue.match_bm25(id, 'crystal') IS NOT NULL
ORDER BY score DESC;

-- Alternative: Search for "dark lord"
-- SELECT * FROM dialogue
-- WHERE fts_main_dialogue.match_bm25(id, 'dark lord') IS NOT NULL;
