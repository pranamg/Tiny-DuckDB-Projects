# Chapter 08: Blackjack Scorer

Calculate blackjack hand scores using JOINs and conditional logic.

## Learning Goals

- Use JOINs to combine data
- Handle complex scoring rules (Ace = 1 or 11)
- Create lookup tables
- Use multiple CASE expressions

## The Challenge

Build a blackjack hand scorer that:
1. Takes a list of cards (e.g., "AS", "KH" for Ace of Spades, King of Hearts)
2. Calculates the optimal score (handling Aces correctly)
3. Determines if the hand is bust, blackjack, or a regular score

## Concepts Introduced

- `JOIN` operations (INNER, LEFT)
- Creating reference tables with VALUES
- Multi-condition `CASE` expressions
- `SUM()` aggregation
- Handling variable card values
