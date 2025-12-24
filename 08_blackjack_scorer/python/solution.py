"""Chapter 08: Blackjack Scorer - Solution."""
import duckdb
from typing import List, Tuple


def get_card_value(rank: str) -> int:
    """
    Get the base value of a card rank.
    
    Args:
        rank: Card rank (A, 2-10, J, Q, K)
        
    Returns:
        Card value (Ace = 11)
    """
    conn = duckdb.connect()
    query = """
    WITH card_values AS (
        SELECT * FROM (VALUES
            ('A', 11), ('2', 2), ('3', 3), ('4', 4), ('5', 5),
            ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10),
            ('J', 10), ('Q', 10), ('K', 10)
        ) AS t(rank, value)
    )
    SELECT value FROM card_values WHERE rank = ?
    """
    result = conn.execute(query, [rank]).fetchone()[0]
    conn.close()
    return result


def parse_card(card: str) -> Tuple[str, str]:
    """
    Parse a card string into rank and suit.
    
    Args:
        card: Card string like "AS" (Ace of Spades) or "10H" (10 of Hearts)
        
    Returns:
        Tuple of (rank, suit)
    """
    conn = duckdb.connect()
    query = """
    SELECT 
        CASE WHEN length(?) = 3 THEN ?[1:2] ELSE ?[1] END as rank,
        ?[-1] as suit
    """
    result = conn.execute(query, [card, card, card, card]).fetchone()
    conn.close()
    return result


def score_hand(cards: List[str]) -> int:
    """
    Calculate the optimal score for a blackjack hand.
    
    Args:
        cards: List of card strings like ["AS", "KH"]
        
    Returns:
        Optimal hand score (adjusting Aces as needed)
    """
    conn = duckdb.connect()
    conn.execute("""
        CREATE TEMP TABLE card_values AS
        SELECT * FROM (VALUES
            ('A', 11), ('2', 2), ('3', 3), ('4', 4), ('5', 5),
            ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10),
            ('J', 10), ('Q', 10), ('K', 10)
        ) AS t(rank, value)
    """)
    conn.execute("CREATE TEMP TABLE hand (card VARCHAR)")
    conn.executemany("INSERT INTO hand VALUES (?)", [(c,) for c in cards])
    
    query = """
    WITH parsed AS (
        SELECT 
            card,
            CASE WHEN length(card) = 3 THEN card[1:2] ELSE card[1] END as rank
        FROM hand
    ),
    scored AS (
        SELECT 
            SUM(cv.value) as total,
            SUM(CASE WHEN p.rank = 'A' THEN 1 ELSE 0 END) as aces
        FROM parsed p
        JOIN card_values cv ON p.rank = cv.rank
    )
    SELECT 
        CASE 
            WHEN total <= 21 THEN total
            ELSE total - (10 * LEAST(aces, (total - 12) / 10 + 1))
        END
    FROM scored
    """
    result = conn.execute(query).fetchone()[0]
    conn.close()
    return result


def get_hand_status(cards: List[str]) -> str:
    """
    Get the status of a blackjack hand.
    
    Args:
        cards: List of card strings
        
    Returns:
        'BLACKJACK!', 'BUST', or 'OK'
    """
    score = score_hand(cards)
    if score > 21:
        return "BUST"
    if score == 21 and len(cards) == 2:
        return "BLACKJACK!"
    return "OK"


def evaluate_hand(cards: List[str]) -> dict:
    """
    Fully evaluate a blackjack hand.
    
    Args:
        cards: List of card strings
        
    Returns:
        Dictionary with cards, score, and status
    """
    return {
        "cards": cards,
        "score": score_hand(cards),
        "status": get_hand_status(cards)
    }


if __name__ == "__main__":
    hands = [
        ["AS", "KH"],           # Blackjack
        ["AS", "5H", "5D"],     # 21
        ["KS", "QH", "5D"],     # Bust (25)
        ["AS", "AS", "9H"],     # 21 (two aces)
    ]
    for hand in hands:
        result = evaluate_hand(hand)
        print(f"{hand}: {result['score']} - {result['status']}")
