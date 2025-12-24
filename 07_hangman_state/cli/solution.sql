-- Chapter 07: Hangman State - Solution
-- Track and display hangman game state

WITH game_state AS (
    SELECT 
        'PYTHON' as secret_word,
        ['P', 'T', 'O', 'X', 'Z'] as guessed_letters
),
letters AS (
    SELECT 
        secret_word,
        guessed_letters,
        generate_subscripts(string_split(secret_word, ''), 1) as pos,
        unnest(string_split(secret_word, '')) as letter
    FROM game_state
)
SELECT 
    secret_word,
    guessed_letters,
    string_agg(
        CASE WHEN letter = ANY(guessed_letters) THEN letter ELSE '_' END, 
        ' ' ORDER BY pos
    ) as display,
    list_filter(guessed_letters, x -> NOT contains(secret_word, x)) as wrong_guesses,
    bool_and(letter = ANY(guessed_letters)) as is_won
FROM letters
GROUP BY secret_word, guessed_letters;
