"""Chapter 05: Anagram Checker - Solution."""
import duckdb


def is_anagram(word1: str, word2: str) -> bool:
    """
    Check if two words are anagrams of each other.
    
    Args:
        word1: First word
        word2: Second word
        
    Returns:
        True if the words are anagrams, False otherwise
    """
    conn = duckdb.connect()
    query = """
    SELECT 
        array_to_string(list_sort(string_split(lower(?), '')), '') =
        array_to_string(list_sort(string_split(lower(?), '')), '')
    """
    result = conn.execute(query, [word1, word2]).fetchone()[0]
    conn.close()
    return result


def find_anagrams(word: str, word_list: list) -> list:
    """
    Find all anagrams of a word from a list.
    
    Args:
        word: The word to find anagrams for
        word_list: List of words to search
        
    Returns:
        List of words that are anagrams
    """
    conn = duckdb.connect()
    conn.execute("CREATE TEMP TABLE words (word VARCHAR)")
    conn.executemany("INSERT INTO words VALUES (?)", [(w,) for w in word_list])
    
    query = """
    WITH target AS (
        SELECT array_to_string(list_sort(string_split(lower(?), '')), '') as sorted_target
    )
    SELECT word
    FROM words, target
    WHERE array_to_string(list_sort(string_split(lower(word), '')), '') = sorted_target
      AND lower(word) != lower(?)
    """
    result = [row[0] for row in conn.execute(query, [word, word]).fetchall()]
    conn.close()
    return result


def sort_letters(word: str) -> str:
    """
    Sort the letters in a word alphabetically.
    
    Args:
        word: The word to sort
        
    Returns:
        String with letters sorted alphabetically
    """
    conn = duckdb.connect()
    query = "SELECT array_to_string(list_sort(string_split(lower(?), '')), '')"
    result = conn.execute(query, [word]).fetchone()[0]
    conn.close()
    return result


if __name__ == "__main__":
    print(f"listen vs silent: {is_anagram('listen', 'silent')}")
    print(f"hello vs world: {is_anagram('hello', 'world')}")
    words = ["listen", "silent", "enlist", "tinsel", "hello"]
    print(f"Anagrams of 'listen': {find_anagrams('listen', words)}")
