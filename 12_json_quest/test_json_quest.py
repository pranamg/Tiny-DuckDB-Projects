"""Tests for Chapter 12: JSON Quest."""
import os
import importlib.util
import duckdb
import pytest

CHAPTER_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CHAPTER_DIR)
SAVE_FILE = os.path.join(PROJECT_ROOT, "inputs", "game_save.json")


def load_solution():
    solution_path = os.path.join(CHAPTER_DIR, "python", "solution.py")
    spec = importlib.util.spec_from_file_location("solution_12", solution_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestPythonTrack:
    def test_get_player_info(self):
        solution = load_solution()
        info = solution.get_player_info(SAVE_FILE)
        assert info["name"] == "DragonSlayer"
        assert info["level"] == 42

    def test_get_inventory(self):
        solution = load_solution()
        items = solution.get_inventory(SAVE_FILE)
        assert len(items) == 5

    def test_get_equipped_items(self):
        solution = load_solution()
        equipped = solution.get_equipped_items(SAVE_FILE)
        assert "Excalibur" in equipped

    def test_get_playtime(self):
        solution = load_solution()
        assert solution.get_playtime(SAVE_FILE) == 127.5


class TestCLITrack:
    def test_solution_sql_executes(self):
        sql_file = os.path.join(CHAPTER_DIR, "cli", "solution.sql")
        conn = duckdb.connect()
        os.chdir(CHAPTER_DIR)
        sql = open(sql_file).read()
        first_query = sql.split(';')[0] + ';'
        result = conn.execute(first_query).fetchone()
        conn.close()
        assert result[0] == "DragonSlayer"


class TestLearnerFiles:
    def test_learner_files_exist(self):
        assert os.path.exists(os.path.join(CHAPTER_DIR, "python", "json_quest.py"))
        assert os.path.exists(os.path.join(CHAPTER_DIR, "cli", "json_quest.sql"))
