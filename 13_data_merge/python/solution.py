"""Chapter 13: Data Merge - Solution."""
import duckdb
from typing import List, Dict, Any, Tuple


def setup_players_table(conn: duckdb.DuckDBPyConnection) -> None:
    """Create and populate the players table."""
    conn.execute("""
        CREATE OR REPLACE TABLE players (
            player_id INTEGER PRIMARY KEY,
            username VARCHAR,
            score INTEGER,
            last_login DATE,
            status VARCHAR DEFAULT 'active'
        )
    """)


def insert_players(conn: duckdb.DuckDBPyConnection, players: List[Tuple]) -> None:
    """Insert players into the table."""
    conn.executemany(
        "INSERT INTO players VALUES (?, ?, ?, ?, ?)",
        players
    )


def merge_player_updates(
    conn: duckdb.DuckDBPyConnection,
    updates: List[Dict[str, Any]]
) -> Dict[str, int]:
    """
    Merge player updates using MERGE statement.
    
    Args:
        conn: Database connection
        updates: List of update dictionaries with player_id, username, score, last_login, status
        
    Returns:
        Dictionary with counts of inserted, updated, deleted
    """
    # Create temp table for updates
    conn.execute("""
        CREATE OR REPLACE TEMP TABLE player_updates (
            player_id INTEGER,
            username VARCHAR,
            score INTEGER,
            last_login DATE,
            status VARCHAR
        )
    """)
    
    for u in updates:
        conn.execute(
            "INSERT INTO player_updates VALUES (?, ?, ?, ?, ?)",
            [u["player_id"], u["username"], u["score"], u["last_login"], u["status"]]
        )
    
    # Count before
    before_count = conn.execute("SELECT COUNT(*) FROM players").fetchone()[0]
    before_ids = set(r[0] for r in conn.execute("SELECT player_id FROM players").fetchall())
    
    # Perform merge
    conn.execute("""
        MERGE INTO players AS target
        USING player_updates AS source
        ON target.player_id = source.player_id
        WHEN MATCHED AND source.status = 'deleted' THEN
            DELETE
        WHEN MATCHED THEN
            UPDATE SET 
                score = source.score,
                last_login = source.last_login,
                status = source.status
        WHEN NOT MATCHED THEN
            INSERT (player_id, username, score, last_login, status)
            VALUES (source.player_id, source.username, source.score, source.last_login, source.status)
    """)
    
    # Count after
    after_count = conn.execute("SELECT COUNT(*) FROM players").fetchone()[0]
    after_ids = set(r[0] for r in conn.execute("SELECT player_id FROM players").fetchall())
    
    inserted = len(after_ids - before_ids)
    deleted = len(before_ids - after_ids)
    updated = len(updates) - inserted - deleted
    
    return {"inserted": inserted, "updated": updated, "deleted": deleted}


def upsert_player(
    conn: duckdb.DuckDBPyConnection,
    player_id: int,
    username: str,
    score: int,
    last_login: str
) -> str:
    """
    Insert or update a single player.
    
    Args:
        conn: Database connection
        player_id: Player ID
        username: Username
        score: Player score
        last_login: Last login date
        
    Returns:
        'inserted' or 'updated'
    """
    existing = conn.execute(
        "SELECT 1 FROM players WHERE player_id = ?", [player_id]
    ).fetchone()
    
    conn.execute(f"""
        MERGE INTO players AS target
        USING (SELECT {player_id} as player_id, '{username}' as username, 
                      {score} as score, '{last_login}'::DATE as last_login, 
                      'active' as status) AS source
        ON target.player_id = source.player_id
        WHEN MATCHED THEN
            UPDATE SET score = source.score, last_login = source.last_login
        WHEN NOT MATCHED THEN
            INSERT VALUES (source.player_id, source.username, source.score, 
                          source.last_login, source.status)
    """)
    
    return "updated" if existing else "inserted"


def get_all_players(conn: duckdb.DuckDBPyConnection) -> List[Dict[str, Any]]:
    """Get all players from the table."""
    result = conn.execute("""
        SELECT player_id, username, score, last_login, status
        FROM players ORDER BY player_id
    """).fetchall()
    return [
        {"player_id": r[0], "username": r[1], "score": r[2], 
         "last_login": str(r[3]), "status": r[4]}
        for r in result
    ]


if __name__ == "__main__":
    conn = duckdb.connect()
    setup_players_table(conn)
    
    # Initial data
    insert_players(conn, [
        (1, "Alice", 1500, "2024-01-15", "active"),
        (2, "Bob", 1200, "2024-01-10", "active"),
        (3, "Charlie", 800, "2023-12-01", "inactive"),
    ])
    
    print("Before merge:")
    for p in get_all_players(conn):
        print(f"  {p}")
    
    # Updates
    updates = [
        {"player_id": 1, "username": "Alice", "score": 1800, "last_login": "2024-01-20", "status": "active"},
        {"player_id": 2, "username": "Bob", "score": 1200, "last_login": "2024-01-10", "status": "deleted"},
        {"player_id": 4, "username": "Diana", "score": 2000, "last_login": "2024-01-19", "status": "active"},
    ]
    
    result = merge_player_updates(conn, updates)
    print(f"\nMerge result: {result}")
    
    print("\nAfter merge:")
    for p in get_all_players(conn):
        print(f"  {p}")
    
    conn.close()
