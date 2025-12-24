# Chapter 04: Number Guesser

Build the logic for a higher/lower guessing game using SQL conditionals.

## Learning Goals

- Use `CASE` expressions for conditional logic
- Work with `random()` function
- Understand comparison in SQL
- Return different results based on conditions

## The Challenge

Create a number guessing game helper that:
1. Generates a random target number (1-100)
2. Takes a guess and returns "Too high!", "Too low!", or "Correct!"
3. Tracks the number of guesses

## Concepts Introduced

- `CASE WHEN ... THEN ... ELSE ... END`
- `random()` function
- `floor()` and `ceil()` for rounding
- `setseed()` for reproducible randomness
- Variable-like behavior with CTEs
