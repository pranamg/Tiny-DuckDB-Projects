# Chapter 11: Sudoku Validator

Validate sudoku boards using complex SQL operations.

## Learning Goals

- Use `PIVOT` and `UNPIVOT` operations
- Validate data with complex constraints
- Work with 2D data structures
- Combine multiple validation rules

## The Challenge

Build a sudoku validator that checks if a completed board is valid:
1. Each row contains 1-9 exactly once
2. Each column contains 1-9 exactly once
3. Each 3x3 box contains 1-9 exactly once

## Concepts Introduced

- `PIVOT` to reshape rows to columns
- `UNPIVOT` to reshape columns to rows
- `COUNT(DISTINCT ...)` for uniqueness checks
- Integer division for box calculations
- Multiple validation CTEs
- `BOOL_AND()` aggregation
