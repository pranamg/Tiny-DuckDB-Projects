"""Tests for Chapter 01: Hello Duck."""
import os
import subprocess
import importlib.util

import duckdb
import pytest

CHAPTER_DIR = os.path.dirname(os.path.abspath(__file__))


def load_solution():
    """Load the solution module dynamically."""
    solution_path = os.path.join(CHAPTER_DIR, "python", "solution.py")
    spec = importlib.util.spec_from_file_location("solution_01", solution_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestPythonTrack:
    """Tests for the Python implementation."""

    def test_solution_returns_correct_greeting(self):
        """The solution should return 'Hello, DuckDB!'."""
        solution = load_solution()
        assert solution.hello() == "Hello, DuckDB!"

    def test_solution_uses_duckdb(self):
        """Verify the solution actually uses DuckDB (not just hardcoded)."""
        conn = duckdb.connect()
        result = conn.execute("SELECT 'Hello, DuckDB!' AS greeting").fetchone()[0]
        conn.close()
        assert result == "Hello, DuckDB!"


class TestCLITrack:
    """Tests for the CLI implementation."""

    def test_solution_sql_returns_correct_greeting(self):
        """The SQL solution should output 'Hello, DuckDB!'."""
        sql_file = os.path.join(CHAPTER_DIR, "cli", "solution.sql")
        result = subprocess.run(
            ["duckdb", "-noheader", "-list"],
            input=open(sql_file).read(),
            capture_output=True,
            text=True,
        )
        assert "Hello, DuckDB!" in result.stdout

    def test_sql_syntax_is_valid(self):
        """The SQL file should have valid syntax."""
        sql_file = os.path.join(CHAPTER_DIR, "cli", "solution.sql")
        conn = duckdb.connect()
        sql = open(sql_file).read()
        conn.execute(sql)
        conn.close()


class TestLearnerFiles:
    """Tests that learners can run against their own implementations."""

    def test_learner_python_file_exists(self):
        """The learner's Python file should exist."""
        py_file = os.path.join(CHAPTER_DIR, "python", "hello.py")
        assert os.path.exists(py_file), "Create python/hello.py to start!"

    def test_learner_sql_file_exists(self):
        """The learner's SQL file should exist."""
        sql_file = os.path.join(CHAPTER_DIR, "cli", "hello.sql")
        assert os.path.exists(sql_file), "Create cli/hello.sql to start!"
