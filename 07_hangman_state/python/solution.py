"""Chapter 07: Hangman State - Solution."""
import duckdb
from typing import Tuple, List


def get_display(secret_word: str, guessed_letters: List[str]) -> str:
    """
    Get the hangman display showing guessed letters and blanks.
    
    Args:
        secret_word: The word to guess
        guessed_letters: List of letters that have been guessed
        
    Returns:
        Display string like "P _ T _ O _"
    """
    conn = duckdb.connect()
    query = """
    WITH letters AS (
        SELECT 
            generate_subscripts(string_split(?, ''), 1) as pos,
            unnest(string_split(upper(?), '')) as letter
    )
    SELECT string_agg(
        CASE WHEN letter = ANY(?) THEN letter ELSE '_' END,
        ' ' ORDER BY pos
    )
    FROM letters
    """
    guessed_upper = [g.upper() for g in guessed_letters]
    result = conn.execute(query, [secret_word, secret_word, guessed_upper]).fetchone()[0]
    conn.close()
    return result


def get_wrong_guesses(secret_word: str, guessed_letters: List[str]) -> List[str]:
    """
    Get list of incorrectly guessed letters.
    
    Args:
        secret_word: The word to guess
        guessed_letters: List of letters that have been guessed
        
    Returns:
        List of wrong guesses
    """
    conn = duckdb.connect()
    query = """
    SELECT list_filter(?, x -> NOT contains(upper(?), x))
    """
    guessed_upper = [g.upper() for g in guessed_letters]
    result = conn.execute(query, [guessed_upper, secret_word]).fetchone()[0]
    conn.close()
    return result if result else []


def is_game_won(secret_word: str, guessed_letters: List[str]) -> bool:
    """
    Check if all letters have been guessed.
    
    Args:
        secret_word: The word to guess
        guessed_letters: List of letters that have been guessed
        
    Returns:
        True if the word is fully revealed
    """
    conn = duckdb.connect()
    query = """
    WITH letters AS (
        SELECT unnest(string_split(upper(?), '')) as letter
    )
    SELECT bool_and(letter = ANY(?))
    FROM letters
    """
    guessed_upper = [g.upper() for g in guessed_letters]
    result = conn.execute(query, [secret_word, guessed_upper]).fetchone()[0]
    conn.close()
    return result


def is_game_lost(wrong_guesses: List[str], max_wrong: int = 6) -> bool:
    """
    Check if too many wrong guesses have been made.
    
    Args:
        wrong_guesses: List of wrong guesses
        max_wrong: Maximum allowed wrong guesses (default 6)
        
    Returns:
        True if game is lost
    """
    conn = duckdb.connect()
    query = "SELECT len(?) >= ?"
    result = conn.execute(query, [wrong_guesses, max_wrong]).fetchone()[0]
    conn.close()
    return result


def get_game_state(secret_word: str, guessed_letters: List[str]) -> dict:
    """
    Get complete game state.
    
    Args:
        secret_word: The word to guess
        guessed_letters: List of letters that have been guessed
        
    Returns:
        Dictionary with display, wrong_guesses, is_won, is_lost
    """
    display = get_display(secret_word, guessed_letters)
    wrong = get_wrong_guesses(secret_word, guessed_letters)
    won = is_game_won(secret_word, guessed_letters)
    lost = is_game_lost(wrong)
    
    return {
        "display": display,
        "wrong_guesses": wrong,
        "is_won": won,
        "is_lost": lost,
        "remaining_lives": 6 - len(wrong)
    }


if __name__ == "__main__":
    state = get_game_state("PYTHON", ["P", "T", "O", "X", "Z"])
    print(f"Display: {state['display']}")
    print(f"Wrong guesses: {state['wrong_guesses']}")
    print(f"Won: {state['is_won']}, Lost: {state['is_lost']}")
    print(f"Lives remaining: {state['remaining_lives']}")
