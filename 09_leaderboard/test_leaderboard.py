"""Tests for Chapter 09: Leaderboard."""
import os
import importlib.util
import duckdb
import pytest

CHAPTER_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CHAPTER_DIR)
SCORES_FILE = os.path.join(PROJECT_ROOT, "inputs", "sample_scores.csv")


def load_solution():
    solution_path = os.path.join(CHAPTER_DIR, "python", "solution.py")
    spec = importlib.util.spec_from_file_location("solution_09", solution_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestPythonTrack:
    def test_get_overall_rankings(self):
        solution = load_solution()
        result = solution.get_overall_rankings(SCORES_FILE)
        assert len(result) > 0
        scores = [r[3] for r in result]
        assert scores == sorted(scores, reverse=True)

    def test_get_rankings_by_game(self):
        solution = load_solution()
        result = solution.get_rankings_by_game(SCORES_FILE)
        games_with_rank1 = set(r[0] for r in result if r[1] == 1)
        assert len(games_with_rank1) >= 2

    def test_get_player_stats(self):
        solution = load_solution()
        result = solution.get_player_stats(SCORES_FILE)
        assert len(result) > 0


class TestCLITrack:
    def test_solution_sql_executes(self):
        sql_file = os.path.join(CHAPTER_DIR, "cli", "solution.sql")
        conn = duckdb.connect()
        os.chdir(CHAPTER_DIR)
        sql = open(sql_file).read()
        result = conn.execute(sql).fetchall()
        conn.close()
        assert len(result) > 0


class TestLearnerFiles:
    def test_learner_files_exist(self):
        assert os.path.exists(os.path.join(CHAPTER_DIR, "python", "leaderboard.py"))
        assert os.path.exists(os.path.join(CHAPTER_DIR, "cli", "leaderboard.sql"))
