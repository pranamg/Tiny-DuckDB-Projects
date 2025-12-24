# Chapter 06: Picnic Planner

Format lists of items with proper grammar using string aggregation.

## Learning Goals

- Aggregate strings with `string_agg()` / `listagg()`
- Handle different list sizes (1, 2, or many items)
- Use conditional formatting
- Build grammatically correct output

## The Challenge

Given a list of items to bring to a picnic, format them correctly:
- 1 item: "chips"
- 2 items: "chips and dip"
- 3+ items: "chips, dip, and salsa"

## Concepts Introduced

- `string_agg()` / `listagg()` aggregation
- `COUNT()` for determining list size
- `CASE` for conditional formatting
- Array functions
- `list_slice()` for sublists
