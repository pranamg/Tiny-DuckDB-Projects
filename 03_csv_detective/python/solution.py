"""Chapter 03: CSV Detective - Solution."""
import duckdb
from typing import List, Tuple, Any


def find_high_scores(filepath: str, threshold: int = 1500) -> List[Tuple[Any, ...]]:
    """
    Find all scores above the given threshold.
    
    Args:
        filepath: Path to the CSV file
        threshold: Minimum score to include
        
    Returns:
        List of (player, game, score, date) tuples
    """
    conn = duckdb.connect()
    query = """
    SELECT player, game, score, date
    FROM read_csv(?)
    WHERE score > ?
    ORDER BY score DESC
    """
    result = conn.execute(query, [filepath, threshold]).fetchall()
    conn.close()
    return result


def find_player_scores(filepath: str, player_name: str) -> List[Tuple[Any, ...]]:
    """
    Find all scores for a specific player.
    
    Args:
        filepath: Path to the CSV file
        player_name: Name of the player to search for
        
    Returns:
        List of (player, game, score, date) tuples
    """
    conn = duckdb.connect()
    query = """
    SELECT player, game, score, date
    FROM read_csv(?)
    WHERE player = ?
    ORDER BY date DESC
    """
    result = conn.execute(query, [filepath, player_name]).fetchall()
    conn.close()
    return result


def find_highest_per_game(filepath: str) -> List[Tuple[str, int]]:
    """
    Find the highest score for each game.
    
    Args:
        filepath: Path to the CSV file
        
    Returns:
        List of (game, highest_score) tuples
    """
    conn = duckdb.connect()
    query = """
    SELECT game, MAX(score) as highest_score
    FROM read_csv(?)
    GROUP BY game
    ORDER BY highest_score DESC
    """
    result = conn.execute(query, [filepath]).fetchall()
    conn.close()
    return result


def find_scores_in_range(filepath: str, min_score: int, max_score: int) -> List[Tuple[Any, ...]]:
    """
    Find all scores within a given range.
    
    Args:
        filepath: Path to the CSV file
        min_score: Minimum score (inclusive)
        max_score: Maximum score (inclusive)
        
    Returns:
        List of (player, game, score, date) tuples
    """
    conn = duckdb.connect()
    query = """
    SELECT player, game, score, date
    FROM read_csv(?)
    WHERE score >= ? AND score <= ?
    ORDER BY score DESC
    """
    result = conn.execute(query, [filepath, min_score, max_score]).fetchall()
    conn.close()
    return result


if __name__ == "__main__":
    import os
    filepath = os.path.join(os.path.dirname(__file__), "..", "..", "inputs", "sample_scores.csv")
    print("High scores (>1500):")
    for row in find_high_scores(filepath):
        print(f"  {row}")
