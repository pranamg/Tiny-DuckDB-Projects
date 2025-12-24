# Chapter 02: Word Counter

Count words in text using DuckDB's aggregation functions.

## Learning Goals

- Use `COUNT()` and `GROUP BY`
- Work with string functions (`string_split`, `unnest`)
- Create tables from values
- Understand aggregation basics

## The Challenge

Given a text string, count how many times each word appears and return the results sorted by count (descending).

### Example

Input: `"the quick brown fox jumps over the lazy dog the"`

Output:
| word  | count |
|-------|-------|
| the   | 3     |
| quick | 1     |
| brown | 1     |
| ...   | ...   |

## Concepts Introduced

- `COUNT(*)` aggregation
- `GROUP BY` clause
- `ORDER BY ... DESC`
- `string_split()` function
- `unnest()` to expand arrays
