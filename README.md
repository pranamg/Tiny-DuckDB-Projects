# Tiny DuckDB Projects

Learning DuckDB through test-driven development of games and puzzles.

Inspired by [Tiny Python Projects](https://github.com/kyclark/tiny_python_projects) and [Tiny PowerShell Projects](https://github.com/dfinke/Tiny-PowerShell-Projects).

## About

This repository teaches DuckDB (v1.4.x) through 15 progressive chapters. Each chapter presents a fun game or puzzle that introduces new SQL concepts. You'll learn by writing code to pass pre-written tests.

**Dual Track Approach:**
- **CLI Track**: Write `.sql` files and run them with the DuckDB CLI
- **Python Track**: Write Python code using the `duckdb` library

## Getting Started

### Prerequisites

- Python 3.9+
- DuckDB CLI (optional, for CLI track)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Tiny-DuckDB-Projects.git
cd Tiny-DuckDB-Projects

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install DuckDB CLI (optional)
# See: https://duckdb.org/docs/installation/
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests for a specific chapter
pytest 01_hello_duck/

# Run with verbose output
pytest -v
```

## Chapters

| # | Chapter | Challenge | Concepts |
|---|---------|-----------|----------|
| 01 | [Hello Duck](01_hello_duck/) | Return a greeting | SELECT, literals, setup |
| 02 | [Word Counter](02_word_counter/) | Count word frequencies | COUNT, GROUP BY, string functions |
| 03 | [CSV Detective](03_csv_detective/) | Query CSV files | read_csv(), WHERE, filtering |
| 04 | [Number Guesser](04_number_guesser/) | Higher/lower game | CASE, random(), conditionals |
| 05 | [Anagram Checker](05_anagram_checker/) | Check for anagrams | String manipulation, sorting |
| 06 | [Picnic Planner](06_picnic_planner/) | Format item lists | string_agg(), LISTAGG |
| 07 | [Hangman State](07_hangman_state/) | Track game state | Subqueries, REPLACE, LIKE |
| 08 | [Blackjack Scorer](08_blackjack_scorer/) | Score card hands | JOINs, CASE, SUM |
| 09 | [Leaderboard](09_leaderboard/) | Rank players | Window functions (RANK, ROW_NUMBER) |
| 10 | [Word Ladder](10_word_ladder/) | Find word paths | Recursive CTEs |
| 11 | [Sudoku Validator](11_sudoku_validator/) | Validate boards | PIVOT/UNPIVOT, complex validation |
| 12 | [JSON Quest](12_json_quest/) | Parse save files | JSON functions, nested data |
| 13 | [Data Merge](13_data_merge/) | Merge profiles | MERGE statement (DuckDB 1.4!) |
| 14 | [Treasure Hunt](14_treasure_hunt/) | Find locations | Spatial extension |
| 15 | [Text Search](15_text_search/) | Search dialogue | Full-text search extension |

## How to Use This Repository

### For Each Chapter:

1. **Read the README** - Understand the challenge and learning goals
2. **Run the tests** - See what's expected: `pytest <chapter>/`
3. **Write your solution**:
   - CLI: Edit `cli/<name>.sql`
   - Python: Edit `python/<name>.py`
4. **Run tests again** - Iterate until all tests pass
5. **Compare with solution** - Check `cli/solution.sql` or `python/solution.py`

### Test-Driven Development

Tests define what "correct" means. The workflow is:

```
RED    -> Run tests, see them fail
GREEN  -> Write code to make tests pass
REFACTOR -> Improve your solution
```

## Project Structure

```
Tiny-DuckDB-Projects/
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── pyproject.toml         # Project configuration
├── conftest.py            # Shared pytest fixtures
├── run_all_tests.py       # Run all chapter tests
├── inputs/                # Shared data files
│
├── 01_hello_duck/         # Chapter directories
│   ├── README.md          # Chapter description
│   ├── cli/
│   │   ├── hello.sql      # Your solution (template)
│   │   └── solution.sql   # Reference solution
│   ├── python/
│   │   ├── hello.py       # Your solution (template)
│   │   └── solution.py    # Reference solution
│   └── test_hello.py      # Tests for this chapter
│
└── ... (chapters 02-15)
```

## DuckDB Resources

- [DuckDB Documentation](https://duckdb.org/docs/)
- [DuckDB Python API](https://duckdb.org/docs/api/python/overview)
- [DuckDB 1.4 Release Notes](https://duckdb.org/2025/09/16/announcing-duckdb-140.html)

## Contributing

Found a bug? Have an idea for a new chapter? Contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run all tests: `pytest`
5. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- Ken Youens-Clark for [Tiny Python Projects](https://github.com/kyclark/tiny_python_projects)
- Doug Finke for [Tiny PowerShell Projects](https://github.com/dfinke/Tiny-PowerShell-Projects)
- The DuckDB team for an amazing database
