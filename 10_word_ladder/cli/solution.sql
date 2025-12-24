-- Chapter 10: Word Ladder - Solution
-- Find word transformation paths using recursive CTEs

-- First, create a table of valid words
CREATE OR REPLACE TEMP TABLE words AS
SELECT column0 as word FROM read_csv('../inputs/four_letter_words.txt', header=false);

-- Function to check if two words differ by exactly one letter
CREATE OR REPLACE TEMP MACRO one_letter_diff(w1, w2) AS (
    length(w1) = length(w2) AND
    (SELECT SUM(CASE WHEN w1[i] != w2[i] THEN 1 ELSE 0 END)
     FROM generate_series(1, length(w1)) as t(i)) = 1
);

-- Find path from 'cold' to 'warm'
WITH RECURSIVE word_path AS (
    -- Base case: start word
    SELECT 
        'cold' as current_word,
        ['cold'] as path,
        1 as depth
    
    UNION ALL
    
    -- Recursive case: find neighbors
    SELECT 
        w.word as current_word,
        list_append(wp.path, w.word) as path,
        wp.depth + 1 as depth
    FROM word_path wp
    JOIN words w ON one_letter_diff(wp.current_word, w.word)
    WHERE NOT list_contains(wp.path, w.word)  -- Avoid cycles
      AND wp.depth < 10  -- Limit search depth
      AND wp.current_word != 'warm'  -- Stop if found
)
SELECT path, depth
FROM word_path
WHERE current_word = 'warm'
ORDER BY depth
LIMIT 1;
