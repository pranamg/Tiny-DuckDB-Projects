# Chapter 12: JSON Quest

Parse and query game save files stored as JSON.

## Learning Goals

- Read and parse JSON data
- Navigate nested JSON structures
- Extract values with JSON path expressions
- Unnest JSON arrays

## The Challenge

Parse a game save file (JSON) to:
1. Extract player stats (name, level, health)
2. List inventory items
3. Find quest progress
4. Calculate total playtime

## Concepts Introduced

- `read_json()` / `read_json_auto()`
- JSON path syntax (`$.field`, `$.array[0]`)
- `json_extract()` and `->` operator
- `json_extract_string()` and `->>` operator
- `unnest()` with JSON arrays
- `json_keys()` and `json_type()`
