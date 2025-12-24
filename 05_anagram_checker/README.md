# Chapter 05: Anagram Checker

Determine if two words are anagrams using string manipulation.

## Learning Goals

- Manipulate strings with SQL functions
- Sort characters within a string
- Compare transformed values
- Use string aggregation

## The Challenge

Write a query that takes two words and determines if they are anagrams (contain the same letters rearranged).

Examples:
- "listen" and "silent" -> TRUE (anagram)
- "hello" and "world" -> FALSE (not anagram)

## Concepts Introduced

- `lower()` for case normalization
- `string_split()` with empty delimiter
- `list_sort()` for sorting arrays
- `list_string_agg()` or `array_to_string()`
- Boolean expressions
