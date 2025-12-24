# Chapter 15: Text Search

Search game dialogue using DuckDB's full-text search extension.

## Learning Goals

- Use the Full-Text Search (FTS) extension
- Create and query text search indexes
- Understand relevance scoring
- Handle stemming and stop words

## The Challenge

Build a game dialogue search system that:
1. Indexes NPC dialogue lines
2. Searches for keywords and phrases
3. Ranks results by relevance
4. Highlights matching terms

## Concepts Introduced

- `INSTALL fts; LOAD fts;`
- `PRAGMA create_fts_index(...)`
- `fts_main_...(...)` table functions
- Match scoring and ranking
- Boolean search operators
- Phrase matching with quotes
- Stemming configuration
