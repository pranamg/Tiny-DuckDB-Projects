-- Chapter 05: Anagram Checker - Solution
-- Check if two words are anagrams

WITH word_analysis AS (
    SELECT 
        'listen' as word1,
        'silent' as word2
),
sorted_chars AS (
    SELECT
        word1,
        word2,
        array_to_string(list_sort(string_split(lower(word1), '')), '') as sorted1,
        array_to_string(list_sort(string_split(lower(word2), '')), '') as sorted2
    FROM word_analysis
)
SELECT 
    word1,
    word2,
    sorted1 = sorted2 as is_anagram
FROM sorted_chars;
