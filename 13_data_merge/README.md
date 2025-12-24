# Chapter 13: Data Merge

Merge player profiles using DuckDB 1.4's new MERGE statement.

## Learning Goals

- Use the `MERGE INTO` statement (new in DuckDB 1.4!)
- Handle insert, update, and delete in one statement
- Match records with complex conditions
- Understand upsert patterns

## The Challenge

Build a player profile merger that:
1. Updates existing player stats when they match
2. Inserts new players that don't exist
3. Optionally deletes players marked as inactive
4. Handles conflicts gracefully

## Concepts Introduced

- `MERGE INTO ... USING ...`
- `WHEN MATCHED THEN UPDATE`
- `WHEN NOT MATCHED THEN INSERT`
- `WHEN MATCHED AND condition THEN DELETE`
- Comparison with INSERT ... ON CONFLICT
- Source and target table concepts
