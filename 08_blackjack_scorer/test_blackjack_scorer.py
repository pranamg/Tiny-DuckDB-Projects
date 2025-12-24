"""Tests for Chapter 08: Blackjack Scorer."""
import os
import importlib.util
import duckdb
import pytest

CHAPTER_DIR = os.path.dirname(os.path.abspath(__file__))


def load_solution():
    solution_path = os.path.join(CHAPTER_DIR, "python", "solution.py")
    spec = importlib.util.spec_from_file_location("solution_08", solution_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestPythonTrack:
    def test_get_card_value(self):
        solution = load_solution()
        assert solution.get_card_value("A") == 11
        assert solution.get_card_value("K") == 10
        assert solution.get_card_value("5") == 5

    def test_score_hand_blackjack(self):
        solution = load_solution()
        assert solution.score_hand(["AS", "KH"]) == 21

    def test_score_hand_ace_adjustment(self):
        solution = load_solution()
        assert solution.score_hand(["AS", "5H", "KD"]) == 16

    def test_get_hand_status_blackjack(self):
        solution = load_solution()
        assert solution.get_hand_status(["AS", "KH"]) == "BLACKJACK!"

    def test_get_hand_status_bust(self):
        solution = load_solution()
        assert solution.get_hand_status(["KS", "QH", "5D"]) == "BUST"


class TestCLITrack:
    def test_solution_sql_executes(self):
        sql_file = os.path.join(CHAPTER_DIR, "cli", "solution.sql")
        conn = duckdb.connect()
        sql = open(sql_file).read()
        result = conn.execute(sql).fetchone()
        conn.close()
        assert result is not None
        assert result[1] == 21


class TestLearnerFiles:
    def test_learner_files_exist(self):
        assert os.path.exists(os.path.join(CHAPTER_DIR, "python", "blackjack_scorer.py"))
        assert os.path.exists(os.path.join(CHAPTER_DIR, "cli", "blackjack_scorer.sql"))
