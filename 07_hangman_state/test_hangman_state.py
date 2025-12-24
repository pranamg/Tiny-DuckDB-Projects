"""Tests for Chapter 07: Hangman State."""
import os
import importlib.util
import duckdb
import pytest

CHAPTER_DIR = os.path.dirname(os.path.abspath(__file__))


def load_solution():
    solution_path = os.path.join(CHAPTER_DIR, "python", "solution.py")
    spec = importlib.util.spec_from_file_location("solution_07", solution_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestPythonTrack:
    def test_get_display_partial(self):
        solution = load_solution()
        result = solution.get_display("PYTHON", ["P", "T", "O"])
        assert result == "P _ T _ O _"

    def test_get_display_none_guessed(self):
        solution = load_solution()
        result = solution.get_display("CAT", [])
        assert result == "_ _ _"

    def test_get_wrong_guesses(self):
        solution = load_solution()
        result = solution.get_wrong_guesses("PYTHON", ["P", "X", "Z", "T"])
        assert "X" in result
        assert "Z" in result

    def test_is_game_won_true(self):
        solution = load_solution()
        assert solution.is_game_won("CAT", ["C", "A", "T"]) == True

    def test_is_game_won_false(self):
        solution = load_solution()
        assert solution.is_game_won("CAT", ["C", "A"]) == False


class TestCLITrack:
    def test_solution_sql_executes(self):
        sql_file = os.path.join(CHAPTER_DIR, "cli", "solution.sql")
        conn = duckdb.connect()
        sql = open(sql_file).read()
        result = conn.execute(sql).fetchone()
        conn.close()
        assert result is not None


class TestLearnerFiles:
    def test_learner_files_exist(self):
        assert os.path.exists(os.path.join(CHAPTER_DIR, "python", "hangman_state.py"))
        assert os.path.exists(os.path.join(CHAPTER_DIR, "cli", "hangman_state.sql"))
