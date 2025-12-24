"""Tests for Chapter 10: Word Ladder."""
import os
import importlib.util
import duckdb
import pytest

CHAPTER_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CHAPTER_DIR)
WORDS_FILE = os.path.join(PROJECT_ROOT, "inputs", "four_letter_words.txt")


def load_solution():
    solution_path = os.path.join(CHAPTER_DIR, "python", "solution.py")
    spec = importlib.util.spec_from_file_location("solution_10", solution_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestPythonTrack:
    def test_one_letter_diff_true(self):
        solution = load_solution()
        assert solution.one_letter_diff("cold", "cord") == True

    def test_one_letter_diff_false(self):
        solution = load_solution()
        assert solution.one_letter_diff("cold", "warm") == False

    def test_find_neighbors(self):
        solution = load_solution()
        conn = duckdb.connect()
        solution.load_words(conn, WORDS_FILE)
        neighbors = solution.find_neighbors(conn, "cold")
        conn.close()
        assert len(neighbors) > 0


class TestCLITrack:
    def test_solution_sql_structure(self):
        sql_file = os.path.join(CHAPTER_DIR, "cli", "solution.sql")
        assert os.path.exists(sql_file)
        sql = open(sql_file).read()
        assert "RECURSIVE" in sql


class TestLearnerFiles:
    def test_learner_files_exist(self):
        assert os.path.exists(os.path.join(CHAPTER_DIR, "python", "word_ladder.py"))
        assert os.path.exists(os.path.join(CHAPTER_DIR, "cli", "word_ladder.sql"))
