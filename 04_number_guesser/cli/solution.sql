-- Chapter 04: Number Guesser - Solution
-- Build a higher/lower guessing game logic

-- Set seed for reproducible results
SELECT setseed(0.42);

-- Generate a target number and evaluate a guess
WITH game AS (
    SELECT 
        floor(random() * 100 + 1)::INTEGER as target,
        50 as guess  -- Example guess
)
SELECT 
    target,
    guess,
    CASE 
        WHEN guess = target THEN 'Correct! You win!'
        WHEN guess < target THEN 'Too low! Guess higher.'
        WHEN guess > target THEN 'Too high! Guess lower.'
    END as result
FROM game;
