-- Chapter 09: Leaderboard - Solution
-- Build a game leaderboard using window functions

WITH scores AS (
    SELECT * FROM read_csv('../inputs/sample_scores.csv')
)
SELECT 
    player,
    game,
    score,
    date,
    ROW_NUMBER() OVER (ORDER BY score DESC) as overall_rank,
    RANK() OVER (PARTITION BY game ORDER BY score DESC) as game_rank,
    DENSE_RANK() OVER (PARTITION BY player ORDER BY score DESC) as personal_rank,
    SUM(score) OVER (PARTITION BY player ORDER BY date) as cumulative_score,
    AVG(score) OVER (PARTITION BY player) as avg_score
FROM scores
ORDER BY overall_rank;
