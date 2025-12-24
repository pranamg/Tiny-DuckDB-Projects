"""Tests for Chapter 15: Text Search."""
import os
import importlib.util
import duckdb
import pytest

CHAPTER_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CHAPTER_DIR)
DIALOGUE_FILE = os.path.join(PROJECT_ROOT, "inputs", "game_dialogue.csv")


def load_solution():
    solution_path = os.path.join(CHAPTER_DIR, "python", "solution.py")
    spec = importlib.util.spec_from_file_location("solution_15", solution_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def fts_conn():
    conn = duckdb.connect()
    try:
        conn.execute("INSTALL fts")
        conn.execute("LOAD fts")
        conn.execute(f"CREATE TABLE dialogue AS SELECT * FROM read_csv('{DIALOGUE_FILE}')")
        conn.execute("PRAGMA create_fts_index('dialogue', 'id', 'dialogue')")
        yield conn
    except Exception as e:
        pytest.skip(f"FTS extension not available: {e}")
    finally:
        conn.close()


class TestPythonTrack:
    def test_get_all_speakers(self, fts_conn):
        solution = load_solution()
        speakers = solution.get_all_speakers(fts_conn)
        assert len(speakers) > 5
        assert "Elder" in speakers

    def test_search_by_location(self, fts_conn):
        solution = load_solution()
        results = solution.search_by_location(fts_conn, "Village Square")
        assert len(results) > 0


class TestLearnerFiles:
    def test_learner_files_exist(self):
        assert os.path.exists(os.path.join(CHAPTER_DIR, "python", "text_search.py"))
        assert os.path.exists(os.path.join(CHAPTER_DIR, "cli", "text_search.sql"))
