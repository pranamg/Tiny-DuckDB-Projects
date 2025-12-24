"""Shared pytest fixtures for Tiny DuckDB Projects."""
import os
import importlib.util
import pytest
import duckdb


@pytest.fixture
def db():
    """Create a fresh in-memory DuckDB connection for each test."""
    conn = duckdb.connect(":memory:")
    yield conn
    conn.close()


@pytest.fixture
def project_root():
    """Return the project root directory."""
    return os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def inputs_dir(project_root):
    """Return the shared inputs directory."""
    return os.path.join(project_root, "inputs")


def load_solution(chapter_dir: str):
    """
    Dynamically load the solution module from a chapter directory.
    
    Args:
        chapter_dir: Path to the chapter directory
        
    Returns:
        The loaded solution module
    """
    solution_path = os.path.join(chapter_dir, "python", "solution.py")
    spec = importlib.util.spec_from_file_location("solution", solution_path)
    solution = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(solution)
    return solution
