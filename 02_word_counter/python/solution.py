"""Chapter 02: Word Counter - Solution."""
import duckdb
from typing import List, Tuple


def count_words(text: str) -> List[Tuple[str, int]]:
    """
    Count word frequencies in the given text.
    
    Args:
        text: The input text to analyze
        
    Returns:
        List of (word, count) tuples sorted by count descending, then word ascending
    """
    conn = duckdb.connect()
    query = """
    WITH words AS (
        SELECT unnest(string_split(lower(?), ' ')) AS word
    )
    SELECT 
        word,
        COUNT(*) AS count
    FROM words
    WHERE word != ''
    GROUP BY word
    ORDER BY count DESC, word ASC
    """
    result = conn.execute(query, [text]).fetchall()
    conn.close()
    return result


def count_words_from_file(filepath: str) -> List[Tuple[str, int]]:
    """
    Count word frequencies from a text file.
    
    Args:
        filepath: Path to the text file
        
    Returns:
        List of (word, count) tuples sorted by count descending
    """
    conn = duckdb.connect()
    query = """
    WITH lines AS (
        SELECT * FROM read_csv(?, columns={'line': 'VARCHAR'}, header=false)
    ),
    words AS (
        SELECT unnest(string_split(lower(line), ' ')) AS word
        FROM lines
    )
    SELECT 
        word,
        COUNT(*) AS count
    FROM words
    WHERE word != '' AND word IS NOT NULL
    GROUP BY word
    ORDER BY count DESC, word ASC
    """
    result = conn.execute(query, [filepath]).fetchall()
    conn.close()
    return result


if __name__ == "__main__":
    text = "the quick brown fox jumps over the lazy dog the"
    for word, count in count_words(text):
        print(f"{word}: {count}")
