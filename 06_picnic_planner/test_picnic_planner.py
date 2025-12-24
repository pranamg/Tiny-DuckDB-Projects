"""Tests for Chapter 06: Picnic Planner."""
import os
import importlib.util
import duckdb
import pytest

CHAPTER_DIR = os.path.dirname(os.path.abspath(__file__))


def load_solution():
    solution_path = os.path.join(CHAPTER_DIR, "python", "solution.py")
    spec = importlib.util.spec_from_file_location("solution_06", solution_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestPythonTrack:
    def test_format_single_item(self):
        solution = load_solution()
        assert solution.format_items(["chips"]) == "chips"

    def test_format_two_items(self):
        solution = load_solution()
        assert solution.format_items(["chips", "dip"]) == "chips and dip"

    def test_format_three_items(self):
        solution = load_solution()
        result = solution.format_items(["chips", "dip", "salsa"])
        assert "chips" in result and "dip" in result and "salsa" in result
        assert "and" in result

    def test_format_empty_list(self):
        solution = load_solution()
        assert solution.format_items([]) == ""


class TestCLITrack:
    def test_solution_sql_executes(self):
        sql_file = os.path.join(CHAPTER_DIR, "cli", "solution.sql")
        conn = duckdb.connect()
        sql = open(sql_file).read()
        result = conn.execute(sql).fetchone()
        conn.close()
        assert result is not None
        assert "and" in result[0]


class TestLearnerFiles:
    def test_learner_files_exist(self):
        assert os.path.exists(os.path.join(CHAPTER_DIR, "python", "picnic_planner.py"))
        assert os.path.exists(os.path.join(CHAPTER_DIR, "cli", "picnic_planner.sql"))
