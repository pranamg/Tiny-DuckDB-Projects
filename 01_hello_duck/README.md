# Chapter 01: Hello Duck

Welcome to your first DuckDB project! This chapter introduces the basics of DuckDB and test-driven development.

## Learning Goals

- Install and set up DuckDB (CLI and Python library)
- Write your first SQL query using SELECT
- Understand how tests work in this project
- Learn the dual-track approach (CLI + Python)

## The Challenge

Write a query that returns the greeting: **"Hello, DuckDB!"**

### CLI Track

Edit `cli/hello.sql` to write a SQL query that outputs "Hello, DuckDB!".

Run your solution:
```bash
duckdb < cli/hello.sql
```

### Python Track

Edit `python/hello.py` to create a function `hello()` that:
1. Connects to DuckDB (in-memory)
2. Executes a query to get "Hello, DuckDB!"
3. Returns the greeting string

## Running Tests

From this directory:
```bash
pytest test_hello.py -v
```

Or from the project root:
```bash
pytest 01_hello_duck/ -v
```

## Hints

<details>
<summary>SQL Hint</summary>

In SQL, you can select a literal string value:
```sql
SELECT 'your text here';
```
</details>

<details>
<summary>Python Hint</summary>

The `duckdb` library lets you execute SQL and fetch results:
```python
import duckdb
conn = duckdb.connect()
result = conn.execute("YOUR SQL HERE").fetchone()[0]
```
</details>

## Concepts Introduced

- `SELECT` statement with literal values
- DuckDB CLI basics (`.read`, running scripts)
- Python `duckdb` library connection
- pytest test structure
