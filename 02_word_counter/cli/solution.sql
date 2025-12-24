-- Chapter 02: Word Counter - Solution
-- Count word frequencies in a text string

WITH words AS (
    SELECT unnest(string_split(lower('the quick brown fox jumps over the lazy dog the'), ' ')) AS word
)
SELECT 
    word,
    COUNT(*) AS count
FROM words
WHERE word != ''
GROUP BY word
ORDER BY count DESC, word ASC;
