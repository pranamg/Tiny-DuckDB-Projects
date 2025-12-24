"""Tests for Chapter 13: Data Merge."""
import os
import importlib.util
import duckdb
import pytest

CHAPTER_DIR = os.path.dirname(os.path.abspath(__file__))


def load_solution():
    solution_path = os.path.join(CHAPTER_DIR, "python", "solution.py")
    spec = importlib.util.spec_from_file_location("solution_13", solution_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestPythonTrack:
    def test_setup_and_insert(self):
        solution = load_solution()
        conn = duckdb.connect()
        solution.setup_players_table(conn)
        solution.insert_players(conn, [
            (1, "Alice", 1000, "2024-01-01", "active"),
        ])
        players = solution.get_all_players(conn)
        assert len(players) == 1
        conn.close()

    def test_merge_updates_existing(self):
        solution = load_solution()
        conn = duckdb.connect()
        solution.setup_players_table(conn)
        solution.insert_players(conn, [(1, "Alice", 1000, "2024-01-01", "active")])
        updates = [{"player_id": 1, "username": "Alice", "score": 2000, 
                   "last_login": "2024-01-15", "status": "active"}]
        solution.merge_player_updates(conn, updates)
        players = solution.get_all_players(conn)
        assert players[0]["score"] == 2000
        conn.close()


class TestCLITrack:
    def test_solution_sql_executes(self):
        sql_file = os.path.join(CHAPTER_DIR, "cli", "solution.sql")
        conn = duckdb.connect()
        sql = open(sql_file).read()
        result = conn.execute(sql).fetchall()
        conn.close()
        assert len(result) > 0


class TestLearnerFiles:
    def test_learner_files_exist(self):
        assert os.path.exists(os.path.join(CHAPTER_DIR, "python", "data_merge.py"))
        assert os.path.exists(os.path.join(CHAPTER_DIR, "cli", "data_merge.sql"))
