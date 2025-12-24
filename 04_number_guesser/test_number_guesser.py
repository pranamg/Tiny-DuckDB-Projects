"""Tests for Chapter 04: Number Guesser."""
import os
import importlib.util
import duckdb
import pytest

CHAPTER_DIR = os.path.dirname(os.path.abspath(__file__))


def load_solution():
    solution_path = os.path.join(CHAPTER_DIR, "python", "solution.py")
    spec = importlib.util.spec_from_file_location("solution_04", solution_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestPythonTrack:
    def test_generate_target_in_range(self):
        solution = load_solution()
        for _ in range(10):
            target = solution.generate_target()
            assert 1 <= target <= 100

    def test_generate_target_with_seed(self):
        solution = load_solution()
        t1 = solution.generate_target(seed=0.5)
        t2 = solution.generate_target(seed=0.5)
        assert t1 == t2

    def test_evaluate_guess_correct(self):
        solution = load_solution()
        result = solution.evaluate_guess(50, 50)
        assert "Correct" in result

    def test_evaluate_guess_too_high(self):
        solution = load_solution()
        result = solution.evaluate_guess(50, 75)
        assert "high" in result.lower()

    def test_evaluate_guess_too_low(self):
        solution = load_solution()
        result = solution.evaluate_guess(50, 25)
        assert "low" in result.lower()

    def test_play_game_stops_on_correct(self):
        solution = load_solution()
        results = solution.play_game(50, [25, 50, 75])
        assert len(results) == 2
        assert "Correct" in results[-1][1]


class TestCLITrack:
    def test_solution_sql_executes(self):
        sql_file = os.path.join(CHAPTER_DIR, "cli", "solution.sql")
        conn = duckdb.connect()
        sql = open(sql_file).read()
        result = conn.execute(sql).fetchall()
        conn.close()
        assert len(result) > 0


class TestLearnerFiles:
    def test_learner_python_file_exists(self):
        assert os.path.exists(os.path.join(CHAPTER_DIR, "python", "number_guesser.py"))

    def test_learner_sql_file_exists(self):
        assert os.path.exists(os.path.join(CHAPTER_DIR, "cli", "number_guesser.sql"))
