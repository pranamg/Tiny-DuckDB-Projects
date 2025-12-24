# Chapter 09: Leaderboard

Build a game leaderboard using window functions.

## Learning Goals

- Use window functions (`RANK`, `ROW_NUMBER`, `DENSE_RANK`)
- Understand `OVER` clause and `PARTITION BY`
- Calculate running totals
- Find top N per group

## The Challenge

Create a leaderboard system that:
1. Ranks players by score
2. Shows rank within each game category
3. Calculates cumulative scores
4. Finds each player's best game

## Concepts Introduced

- `ROW_NUMBER() OVER (...)`
- `RANK()` vs `DENSE_RANK()`
- `PARTITION BY` for grouping
- `ORDER BY` within window
- `SUM() OVER (...)` for running totals
- `FIRST_VALUE()`, `LAST_VALUE()`
