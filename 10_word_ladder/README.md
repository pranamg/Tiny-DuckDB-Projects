# Chapter 10: Word Ladder

Find word transformation paths using recursive CTEs.

## Learning Goals

- Write recursive Common Table Expressions (CTEs)
- Understand graph-like traversal in SQL
- Build path-finding queries
- Handle cycles and termination conditions

## The Challenge

Build a word ladder solver that finds a path from one word to another by changing one letter at a time:

Example: "cold" -> "warm"
- cold -> cord -> card -> ward -> warm

## Concepts Introduced

- `WITH RECURSIVE` syntax
- Base case and recursive case
- Cycle detection
- Path accumulation
- `UNION ALL` in recursion
- Termination conditions
