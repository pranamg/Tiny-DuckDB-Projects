"""Chapter 09: Leaderboard - Solution."""
import duckdb
from typing import List, Tuple, Any


def get_overall_rankings(filepath: str) -> List[Tuple[Any, ...]]:
    """
    Get overall rankings sorted by score.
    
    Args:
        filepath: Path to scores CSV
        
    Returns:
        List of (rank, player, game, score) tuples
    """
    conn = duckdb.connect()
    query = """
    SELECT 
        ROW_NUMBER() OVER (ORDER BY score DESC) as rank,
        player,
        game,
        score
    FROM read_csv(?)
    ORDER BY rank
    """
    result = conn.execute(query, [filepath]).fetchall()
    conn.close()
    return result


def get_rankings_by_game(filepath: str) -> List[Tuple[Any, ...]]:
    """
    Get rankings within each game.
    
    Args:
        filepath: Path to scores CSV
        
    Returns:
        List of (game, rank, player, score) tuples
    """
    conn = duckdb.connect()
    query = """
    SELECT 
        game,
        RANK() OVER (PARTITION BY game ORDER BY score DESC) as rank,
        player,
        score
    FROM read_csv(?)
    ORDER BY game, rank
    """
    result = conn.execute(query, [filepath]).fetchall()
    conn.close()
    return result


def get_player_cumulative_scores(filepath: str, player: str) -> List[Tuple[Any, ...]]:
    """
    Get cumulative scores over time for a player.
    
    Args:
        filepath: Path to scores CSV
        player: Player name
        
    Returns:
        List of (date, game, score, cumulative_score) tuples
    """
    conn = duckdb.connect()
    query = """
    SELECT 
        date,
        game,
        score,
        SUM(score) OVER (ORDER BY date) as cumulative_score
    FROM read_csv(?)
    WHERE player = ?
    ORDER BY date
    """
    result = conn.execute(query, [filepath, player]).fetchall()
    conn.close()
    return result


def get_top_n_per_game(filepath: str, n: int = 3) -> List[Tuple[Any, ...]]:
    """
    Get top N players for each game.
    
    Args:
        filepath: Path to scores CSV
        n: Number of top players per game
        
    Returns:
        List of (game, rank, player, score) tuples
    """
    conn = duckdb.connect()
    query = """
    WITH ranked AS (
        SELECT 
            game,
            RANK() OVER (PARTITION BY game ORDER BY score DESC) as rank,
            player,
            score
        FROM read_csv(?)
    )
    SELECT * FROM ranked WHERE rank <= ?
    ORDER BY game, rank
    """
    result = conn.execute(query, [filepath, n]).fetchall()
    conn.close()
    return result


def get_player_stats(filepath: str) -> List[Tuple[Any, ...]]:
    """
    Get statistics for each player.
    
    Args:
        filepath: Path to scores CSV
        
    Returns:
        List of (player, games_played, total_score, avg_score, best_score) tuples
    """
    conn = duckdb.connect()
    query = """
    SELECT 
        player,
        COUNT(*) as games_played,
        SUM(score) as total_score,
        ROUND(AVG(score), 2) as avg_score,
        MAX(score) as best_score,
        MIN(score) as worst_score
    FROM read_csv(?)
    GROUP BY player
    ORDER BY total_score DESC
    """
    result = conn.execute(query, [filepath]).fetchall()
    conn.close()
    return result


def get_player_best_game(filepath: str, player: str) -> Tuple[Any, ...]:
    """
    Get a player's best game using FIRST_VALUE.
    
    Args:
        filepath: Path to scores CSV
        player: Player name
        
    Returns:
        Tuple of (game, score, date) for best performance
    """
    conn = duckdb.connect()
    query = """
    SELECT DISTINCT
        FIRST_VALUE(game) OVER (ORDER BY score DESC) as best_game,
        FIRST_VALUE(score) OVER (ORDER BY score DESC) as best_score,
        FIRST_VALUE(date) OVER (ORDER BY score DESC) as best_date
    FROM read_csv(?)
    WHERE player = ?
    """
    result = conn.execute(query, [filepath, player]).fetchone()
    conn.close()
    return result


if __name__ == "__main__":
    import os
    filepath = os.path.join(os.path.dirname(__file__), "..", "..", "inputs", "sample_scores.csv")
    
    print("Overall Rankings:")
    for row in get_overall_rankings(filepath)[:5]:
        print(f"  #{row[0]}: {row[1]} - {row[2]} ({row[3]} pts)")
    
    print("\nPlayer Stats:")
    for row in get_player_stats(filepath):
        print(f"  {row[0]}: {row[2]} total, {row[3]} avg")
