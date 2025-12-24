"""Tests for Chapter 02: Word Counter."""
import os
import importlib.util
import duckdb
import pytest

CHAPTER_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CHAPTER_DIR)


def load_solution():
    solution_path = os.path.join(CHAPTER_DIR, "python", "solution.py")
    spec = importlib.util.spec_from_file_location("solution_02", solution_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestPythonTrack:
    def test_count_words_basic(self):
        solution = load_solution()
        result = solution.count_words("the quick brown fox jumps over the lazy dog the")
        result_dict = {word: count for word, count in result}
        assert result_dict["the"] == 3
        assert result_dict["fox"] == 1

    def test_count_words_sorted_by_count(self):
        solution = load_solution()
        result = solution.count_words("a a a b b c")
        assert result[0] == ("a", 3)
        assert result[1] == ("b", 2)
        assert result[2] == ("c", 1)

    def test_count_words_case_insensitive(self):
        solution = load_solution()
        result = solution.count_words("The THE the")
        result_dict = {word: count for word, count in result}
        assert result_dict["the"] == 3

    def test_count_words_empty_string(self):
        solution = load_solution()
        result = solution.count_words("")
        assert result == []

    def test_count_words_from_file(self):
        solution = load_solution()
        filepath = os.path.join(PROJECT_ROOT, "inputs", "sample_text.txt")
        result = solution.count_words_from_file(filepath)
        result_dict = {word: count for word, count in result}
        assert result_dict["the"] >= 5


class TestCLITrack:
    def test_solution_sql_executes(self):
        sql_file = os.path.join(CHAPTER_DIR, "cli", "solution.sql")
        conn = duckdb.connect()
        sql = open(sql_file).read()
        result = conn.execute(sql).fetchall()
        conn.close()
        assert len(result) > 0

    def test_solution_sql_returns_word_counts(self):
        sql_file = os.path.join(CHAPTER_DIR, "cli", "solution.sql")
        conn = duckdb.connect()
        sql = open(sql_file).read()
        result = conn.execute(sql).fetchall()
        conn.close()
        result_dict = {row[0]: row[1] for row in result}
        assert result_dict["the"] == 3


class TestLearnerFiles:
    def test_learner_python_file_exists(self):
        assert os.path.exists(os.path.join(CHAPTER_DIR, "python", "word_counter.py"))

    def test_learner_sql_file_exists(self):
        assert os.path.exists(os.path.join(CHAPTER_DIR, "cli", "word_counter.sql"))
