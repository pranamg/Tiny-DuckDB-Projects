"""Chapter 10: Word Ladder - Solution."""
import duckdb
from typing import List, Optional
import os


def load_words(conn: duckdb.DuckDBPyConnection, filepath: str) -> None:
    """Load words from file into a temp table."""
    conn.execute(f"""
        CREATE OR REPLACE TEMP TABLE words AS
        SELECT column0 as word FROM read_csv('{filepath}', header=false)
    """)


def one_letter_diff(word1: str, word2: str) -> bool:
    """
    Check if two words differ by exactly one letter.
    
    Args:
        word1: First word
        word2: Second word
        
    Returns:
        True if words differ by exactly one letter
    """
    conn = duckdb.connect()
    query = """
    SELECT 
        length(?) = length(?) AND
        (SELECT SUM(CASE WHEN ?[i] != ?[i] THEN 1 ELSE 0 END)
         FROM generate_series(1, length(?)) as t(i)) = 1
    """
    result = conn.execute(query, [word1, word2, word1, word2, word1]).fetchone()[0]
    conn.close()
    return result


def find_neighbors(conn: duckdb.DuckDBPyConnection, word: str) -> List[str]:
    """
    Find all valid words that differ by one letter.
    
    Args:
        conn: Database connection with words table
        word: Word to find neighbors for
        
    Returns:
        List of neighboring words
    """
    query = """
    SELECT word
    FROM words
    WHERE length(word) = length(?)
      AND (SELECT SUM(CASE WHEN word[i] != ?[i] THEN 1 ELSE 0 END)
           FROM generate_series(1, length(?)) as t(i)) = 1
    """
    result = [row[0] for row in conn.execute(query, [word, word, word]).fetchall()]
    return result


def find_word_ladder(
    start: str, 
    end: str, 
    filepath: str,
    max_depth: int = 10
) -> Optional[List[str]]:
    """
    Find shortest path from start word to end word.
    
    Args:
        start: Starting word
        end: Target word
        filepath: Path to word list file
        max_depth: Maximum search depth
        
    Returns:
        List of words forming the path, or None if no path found
    """
    conn = duckdb.connect()
    load_words(conn, filepath)
    
    query = f"""
    WITH RECURSIVE word_path AS (
        SELECT 
            '{start}' as current_word,
            ['{start}'] as path,
            1 as depth
        
        UNION ALL
        
        SELECT 
            w.word as current_word,
            list_append(wp.path, w.word) as path,
            wp.depth + 1 as depth
        FROM word_path wp
        JOIN words w ON (
            length(w.word) = length(wp.current_word) AND
            (SELECT SUM(CASE WHEN w.word[i] != wp.current_word[i] THEN 1 ELSE 0 END)
             FROM generate_series(1, length(wp.current_word)) as t(i)) = 1
        )
        WHERE NOT list_contains(wp.path, w.word)
          AND wp.depth < {max_depth}
          AND wp.current_word != '{end}'
    )
    SELECT path
    FROM word_path
    WHERE current_word = '{end}'
    ORDER BY depth
    LIMIT 1
    """
    
    result = conn.execute(query).fetchone()
    conn.close()
    
    return list(result[0]) if result else None


def find_all_paths(
    start: str, 
    end: str, 
    filepath: str,
    max_depth: int = 8
) -> List[List[str]]:
    """
    Find all paths from start to end within max_depth.
    
    Args:
        start: Starting word
        end: Target word
        filepath: Path to word list file
        max_depth: Maximum search depth
        
    Returns:
        List of all valid paths
    """
    conn = duckdb.connect()
    load_words(conn, filepath)
    
    query = f"""
    WITH RECURSIVE word_path AS (
        SELECT 
            '{start}' as current_word,
            ['{start}'] as path,
            1 as depth
        
        UNION ALL
        
        SELECT 
            w.word as current_word,
            list_append(wp.path, w.word) as path,
            wp.depth + 1 as depth
        FROM word_path wp
        JOIN words w ON (
            length(w.word) = length(wp.current_word) AND
            (SELECT SUM(CASE WHEN w.word[i] != wp.current_word[i] THEN 1 ELSE 0 END)
             FROM generate_series(1, length(wp.current_word)) as t(i)) = 1
        )
        WHERE NOT list_contains(wp.path, w.word)
          AND wp.depth < {max_depth}
          AND wp.current_word != '{end}'
    )
    SELECT path
    FROM word_path
    WHERE current_word = '{end}'
    ORDER BY depth
    """
    
    result = [list(row[0]) for row in conn.execute(query).fetchall()]
    conn.close()
    return result


if __name__ == "__main__":
    filepath = os.path.join(os.path.dirname(__file__), "..", "..", "inputs", "four_letter_words.txt")
    
    print("Finding path from 'cold' to 'warm':")
    path = find_word_ladder("cold", "warm", filepath)
    if path:
        print(" -> ".join(path))
    else:
        print("No path found")
    
    print("\nFinding path from 'head' to 'tail':")
    path = find_word_ladder("head", "tail", filepath)
    if path:
        print(" -> ".join(path))
    else:
        print("No path found")
