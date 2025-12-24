"""Tests for Chapter 14: Treasure Hunt."""
import os
import importlib.util
import duckdb
import pytest

CHAPTER_DIR = os.path.dirname(os.path.abspath(__file__))


def load_solution():
    solution_path = os.path.join(CHAPTER_DIR, "python", "solution.py")
    spec = importlib.util.spec_from_file_location("solution_14", solution_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture
def spatial_conn():
    conn = duckdb.connect()
    try:
        conn.execute("INSTALL spatial")
        conn.execute("LOAD spatial")
        yield conn
    except Exception:
        pytest.skip("Spatial extension not available")
    finally:
        conn.close()


class TestPythonTrack:
    def test_add_and_find_treasure(self, spatial_conn):
        solution = load_solution()
        solution.create_treasures_table(spatial_conn)
        solution.add_treasure(spatial_conn, 1, "Gold", 10.0, 20.0, 1000)
        treasures = solution.get_treasure_locations(spatial_conn)
        assert len(treasures) == 1

    def test_find_treasures_nearby(self, spatial_conn):
        solution = load_solution()
        solution.create_treasures_table(spatial_conn)
        solution.add_treasure(spatial_conn, 1, "Near", 11.0, 20.0, 100)
        solution.add_treasure(spatial_conn, 2, "Far", 50.0, 50.0, 100)
        nearby = solution.find_treasures_nearby(spatial_conn, 10.0, 20.0, 5.0)
        assert len(nearby) == 1


class TestLearnerFiles:
    def test_learner_files_exist(self):
        assert os.path.exists(os.path.join(CHAPTER_DIR, "python", "treasure_hunt.py"))
        assert os.path.exists(os.path.join(CHAPTER_DIR, "cli", "treasure_hunt.sql"))
