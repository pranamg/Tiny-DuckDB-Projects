"""Tests for Chapter 05: Anagram Checker."""
import os
import importlib.util
import duckdb
import pytest

CHAPTER_DIR = os.path.dirname(os.path.abspath(__file__))


def load_solution():
    solution_path = os.path.join(CHAPTER_DIR, "python", "solution.py")
    spec = importlib.util.spec_from_file_location("solution_05", solution_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestPythonTrack:
    def test_is_anagram_true(self):
        solution = load_solution()
        assert solution.is_anagram("listen", "silent") == True
        assert solution.is_anagram("evil", "vile") == True

    def test_is_anagram_false(self):
        solution = load_solution()
        assert solution.is_anagram("hello", "world") == False

    def test_is_anagram_case_insensitive(self):
        solution = load_solution()
        assert solution.is_anagram("Listen", "Silent") == True

    def test_is_anagram_same_word(self):
        solution = load_solution()
        assert solution.is_anagram("test", "test") == True

    def test_find_anagrams(self):
        solution = load_solution()
        words = ["listen", "silent", "enlist", "hello"]
        result = solution.find_anagrams("listen", words)
        assert "silent" in result
        assert "enlist" in result
        assert "hello" not in result

    def test_sort_letters(self):
        solution = load_solution()
        assert solution.sort_letters("hello") == "ehllo"


class TestCLITrack:
    def test_solution_sql_executes(self):
        sql_file = os.path.join(CHAPTER_DIR, "cli", "solution.sql")
        conn = duckdb.connect()
        sql = open(sql_file).read()
        result = conn.execute(sql).fetchone()
        conn.close()
        assert result is not None
        assert result[2] == True  # is_anagram


class TestLearnerFiles:
    def test_learner_files_exist(self):
        assert os.path.exists(os.path.join(CHAPTER_DIR, "python", "anagram_checker.py"))
        assert os.path.exists(os.path.join(CHAPTER_DIR, "cli", "anagram_checker.sql"))
