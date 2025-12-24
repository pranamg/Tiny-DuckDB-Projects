# Chapter 07: Hangman State

Track and display the state of a Hangman game using SQL.

## Learning Goals

- Use subqueries for complex logic
- Work with `REPLACE()` and pattern matching
- Track game state with SQL
- Use `LIKE` for pattern matching

## The Challenge

Build a Hangman state tracker that:
1. Takes a secret word and list of guessed letters
2. Shows the current display (e.g., "_ A _ _ M A _")
3. Lists wrong guesses
4. Determines if the game is won or lost

## Concepts Introduced

- Subqueries (scalar and table)
- `REPLACE()` function
- `LIKE` pattern matching
- `regexp_replace()` for complex patterns
- Character-by-character processing
