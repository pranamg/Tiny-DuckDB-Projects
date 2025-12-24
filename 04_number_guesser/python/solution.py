"""Chapter 04: Number Guesser - Solution."""
import duckdb
from typing import Tuple


def generate_target(seed: float = None) -> int:
    """
    Generate a random target number between 1 and 100.
    
    Args:
        seed: Optional seed for reproducibility
        
    Returns:
        Random integer between 1 and 100
    """
    conn = duckdb.connect()
    if seed is not None:
        conn.execute(f"SELECT setseed({seed})")
    result = conn.execute("SELECT floor(random() * 100 + 1)::INTEGER").fetchone()[0]
    conn.close()
    return result


def evaluate_guess(target: int, guess: int) -> str:
    """
    Evaluate a guess against the target number.
    
    Args:
        target: The target number to guess
        guess: The player's guess
        
    Returns:
        Feedback string: "Correct!", "Too high!", or "Too low!"
    """
    conn = duckdb.connect()
    query = """
    SELECT CASE 
        WHEN ? = ? THEN 'Correct! You win!'
        WHEN ? < ? THEN 'Too low! Guess higher.'
        WHEN ? > ? THEN 'Too high! Guess lower.'
    END
    """
    result = conn.execute(query, [guess, target, guess, target, guess, target]).fetchone()[0]
    conn.close()
    return result


def play_game(target: int, guesses: list) -> list:
    """
    Play a number guessing game with multiple guesses.
    
    Args:
        target: The target number
        guesses: List of guesses to evaluate
        
    Returns:
        List of (guess, result) tuples
    """
    conn = duckdb.connect()
    results = []
    for guess in guesses:
        result = evaluate_guess(target, guess)
        results.append((guess, result))
        if "Correct" in result:
            break
    return results


def count_guesses_to_win(target: int, guesses: list) -> int:
    """
    Count how many guesses it took to find the target.
    
    Args:
        target: The target number
        guesses: List of guesses made
        
    Returns:
        Number of guesses (or -1 if not found)
    """
    conn = duckdb.connect()
    query = """
    WITH numbered_guesses AS (
        SELECT 
            unnest(?) as guess,
            generate_subscripts(?, 1) as attempt
    )
    SELECT MIN(attempt)
    FROM numbered_guesses
    WHERE guess = ?
    """
    result = conn.execute(query, [guesses, guesses, target]).fetchone()[0]
    conn.close()
    return result if result else -1


if __name__ == "__main__":
    target = generate_target(seed=0.42)
    print(f"Target: {target}")
    guesses = [50, 75, 60, 65, target]
    for guess, result in play_game(target, guesses):
        print(f"Guess {guess}: {result}")
