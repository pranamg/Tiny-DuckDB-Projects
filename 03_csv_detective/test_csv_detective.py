"""Tests for Chapter 03: CSV Detective."""
import os
import importlib.util
import duckdb
import pytest

CHAPTER_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CHAPTER_DIR)
SCORES_FILE = os.path.join(PROJECT_ROOT, "inputs", "sample_scores.csv")


def load_solution():
    solution_path = os.path.join(CHAPTER_DIR, "python", "solution.py")
    spec = importlib.util.spec_from_file_location("solution_03", solution_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestPythonTrack:
    def test_find_high_scores(self):
        solution = load_solution()
        result = solution.find_high_scores(SCORES_FILE, 1500)
        assert len(result) > 0
        assert all(row[2] > 1500 for row in result)

    def test_find_high_scores_sorted(self):
        solution = load_solution()
        result = solution.find_high_scores(SCORES_FILE, 1000)
        scores = [row[2] for row in result]
        assert scores == sorted(scores, reverse=True)

    def test_find_player_scores(self):
        solution = load_solution()
        result = solution.find_player_scores(SCORES_FILE, "Alice")
        assert len(result) > 0
        assert all(row[0] == "Alice" for row in result)

    def test_find_highest_per_game(self):
        solution = load_solution()
        result = solution.find_highest_per_game(SCORES_FILE)
        result_dict = {row[0]: row[1] for row in result}
        assert "Puzzle Quest" in result_dict

    def test_find_scores_in_range(self):
        solution = load_solution()
        result = solution.find_scores_in_range(SCORES_FILE, 1500, 2000)
        assert len(result) > 0
        assert all(1500 <= row[2] <= 2000 for row in result)


class TestCLITrack:
    def test_solution_sql_executes(self):
        sql_file = os.path.join(CHAPTER_DIR, "cli", "solution.sql")
        conn = duckdb.connect()
        os.chdir(CHAPTER_DIR)
        sql = open(sql_file).read()
        first_query = sql.split(';')[0] + ';'
        result = conn.execute(first_query).fetchall()
        conn.close()
        assert len(result) > 0


class TestLearnerFiles:
    def test_learner_python_file_exists(self):
        assert os.path.exists(os.path.join(CHAPTER_DIR, "python", "csv_detective.py"))

    def test_learner_sql_file_exists(self):
        assert os.path.exists(os.path.join(CHAPTER_DIR, "cli", "csv_detective.sql"))
