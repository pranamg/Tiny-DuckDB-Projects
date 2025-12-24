"""Chapter 15: Text Search - Solution."""
import duckdb
from typing import List, Dict, Any


def setup_fts(conn: duckdb.DuckDBPyConnection) -> None:
    """Install and load FTS extension."""
    conn.execute("INSTALL fts")
    conn.execute("LOAD fts")


def load_dialogue(conn: duckdb.DuckDBPyConnection, filepath: str) -> None:
    """Load dialogue from CSV file."""
    conn.execute(f"""
        CREATE OR REPLACE TABLE dialogue AS
        SELECT * FROM read_csv('{filepath}')
    """)


def create_fts_index(conn: duckdb.DuckDBPyConnection) -> None:
    """Create full-text search index on dialogue."""
    conn.execute("PRAGMA create_fts_index('dialogue', 'id', 'dialogue')")


def search_dialogue(
    conn: duckdb.DuckDBPyConnection,
    query: str
) -> List[Dict[str, Any]]:
    """
    Search dialogue using full-text search.
    
    Args:
        conn: Database connection
        query: Search query string
        
    Returns:
        List of matching dialogue entries with scores
    """
    sql = f"""
    SELECT 
        id,
        speaker,
        location,
        dialogue,
        fts_main_dialogue.match_bm25(id, '{query}') as score
    FROM dialogue
    WHERE fts_main_dialogue.match_bm25(id, '{query}') IS NOT NULL
    ORDER BY score DESC
    """
    result = conn.execute(sql).fetchall()
    return [
        {"id": r[0], "speaker": r[1], "location": r[2], "dialogue": r[3], "score": r[4]}
        for r in result
    ]


def search_by_speaker(
    conn: duckdb.DuckDBPyConnection,
    speaker: str,
    query: str = None
) -> List[Dict[str, Any]]:
    """
    Search dialogue from a specific speaker.
    
    Args:
        conn: Database connection
        speaker: Speaker name
        query: Optional search query
        
    Returns:
        List of matching dialogue entries
    """
    if query:
        sql = f"""
        SELECT id, speaker, location, dialogue
        FROM dialogue
        WHERE speaker = '{speaker}'
          AND fts_main_dialogue.match_bm25(id, '{query}') IS NOT NULL
        """
    else:
        sql = f"""
        SELECT id, speaker, location, dialogue
        FROM dialogue
        WHERE speaker = '{speaker}'
        """
    result = conn.execute(sql).fetchall()
    return [{"id": r[0], "speaker": r[1], "location": r[2], "dialogue": r[3]} for r in result]


def search_by_location(
    conn: duckdb.DuckDBPyConnection,
    location: str
) -> List[Dict[str, Any]]:
    """
    Get all dialogue from a specific location.
    
    Args:
        conn: Database connection
        location: Location name
        
    Returns:
        List of dialogue entries
    """
    sql = f"""
    SELECT id, speaker, location, dialogue
    FROM dialogue
    WHERE location = '{location}'
    ORDER BY id
    """
    result = conn.execute(sql).fetchall()
    return [{"id": r[0], "speaker": r[1], "location": r[2], "dialogue": r[3]} for r in result]


def get_all_speakers(conn: duckdb.DuckDBPyConnection) -> List[str]:
    """Get list of all unique speakers."""
    result = conn.execute("SELECT DISTINCT speaker FROM dialogue ORDER BY speaker").fetchall()
    return [r[0] for r in result]


def get_all_locations(conn: duckdb.DuckDBPyConnection) -> List[str]:
    """Get list of all unique locations."""
    result = conn.execute("SELECT DISTINCT location FROM dialogue ORDER BY location").fetchall()
    return [r[0] for r in result]


def count_keyword_occurrences(
    conn: duckdb.DuckDBPyConnection,
    keyword: str
) -> int:
    """
    Count how many dialogue entries contain a keyword.
    
    Args:
        conn: Database connection
        keyword: Keyword to search for
        
    Returns:
        Count of matching entries
    """
    sql = f"""
    SELECT COUNT(*)
    FROM dialogue
    WHERE fts_main_dialogue.match_bm25(id, '{keyword}') IS NOT NULL
    """
    return conn.execute(sql).fetchone()[0]


if __name__ == "__main__":
    import os
    filepath = os.path.join(os.path.dirname(__file__), "..", "..", "inputs", "game_dialogue.csv")
    
    conn = duckdb.connect()
    setup_fts(conn)
    load_dialogue(conn, filepath)
    create_fts_index(conn)
    
    print("Searching for 'crystal':")
    for entry in search_dialogue(conn, "crystal"):
        print(f"  [{entry['speaker']}] {entry['dialogue'][:50]}... (score: {entry['score']:.2f})")
    
    print("\nSearching for 'dark lord':")
    for entry in search_dialogue(conn, "dark lord"):
        print(f"  [{entry['speaker']}] {entry['dialogue'][:50]}...")
    
    print("\nAll dialogue from Village Square:")
    for entry in search_by_location(conn, "Village Square"):
        print(f"  [{entry['speaker']}] {entry['dialogue'][:50]}...")
    
    conn.close()
