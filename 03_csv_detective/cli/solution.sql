-- Chapter 03: CSV Detective - Solution
-- Query CSV files to find clues in game score data

-- Query 1: Find all scores above 1500
SELECT player, game, score, date
FROM read_csv('../inputs/sample_scores.csv')
WHERE score > 1500
ORDER BY score DESC;

-- Query 2: Find all scores for a specific player
-- SELECT player, game, score, date
-- FROM read_csv('../inputs/sample_scores.csv')
-- WHERE player = 'Alice';

-- Query 3: Find highest score per game
-- SELECT game, MAX(score) as highest_score
-- FROM read_csv('../inputs/sample_scores.csv')
-- GROUP BY game;
