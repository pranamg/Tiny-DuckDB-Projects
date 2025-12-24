"""Chapter 12: JSON Quest - Solution."""
import duckdb
from typing import Any, Dict, List


def load_save_file(filepath: str) -> Dict[str, Any]:
    """
    Load a game save file and return as dictionary.
    
    Args:
        filepath: Path to JSON save file
        
    Returns:
        Dictionary with save data
    """
    conn = duckdb.connect()
    query = f"SELECT * FROM read_json('{filepath}')"
    result = conn.execute(query).fetchone()
    conn.close()
    # Convert to dict
    desc = conn.execute(query).description
    return dict(zip([d[0] for d in conn.execute(query).description], result)) if result else {}


def get_player_info(filepath: str) -> Dict[str, Any]:
    """
    Extract player information from save file.
    
    Args:
        filepath: Path to JSON save file
        
    Returns:
        Dictionary with player stats
    """
    conn = duckdb.connect()
    query = f"""
    SELECT 
        player.name as name,
        player.level as level,
        player.class as class,
        player.health as health,
        player.max_health as max_health,
        player.mana as mana,
        player.max_mana as max_mana
    FROM read_json('{filepath}')
    """
    result = conn.execute(query).fetchone()
    columns = ["name", "level", "class", "health", "max_health", "mana", "max_mana"]
    conn.close()
    return dict(zip(columns, result)) if result else {}


def get_inventory(filepath: str) -> List[Dict[str, Any]]:
    """
    Extract inventory items from save file.
    
    Args:
        filepath: Path to JSON save file
        
    Returns:
        List of inventory item dictionaries
    """
    conn = duckdb.connect()
    query = f"""
    SELECT 
        item.id,
        item.name,
        item.type,
        item.equipped
    FROM (
        SELECT unnest(inventory) as item 
        FROM read_json('{filepath}')
    )
    """
    result = conn.execute(query).fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "type": r[2], "equipped": r[3]} for r in result]


def get_equipped_items(filepath: str) -> List[str]:
    """
    Get names of equipped items.
    
    Args:
        filepath: Path to JSON save file
        
    Returns:
        List of equipped item names
    """
    conn = duckdb.connect()
    query = f"""
    SELECT item.name
    FROM (
        SELECT unnest(inventory) as item 
        FROM read_json('{filepath}')
    )
    WHERE item.equipped = true
    """
    result = [r[0] for r in conn.execute(query).fetchall()]
    conn.close()
    return result


def get_active_quests(filepath: str) -> List[Dict[str, Any]]:
    """
    Get active quests and their progress.
    
    Args:
        filepath: Path to JSON save file
        
    Returns:
        List of quest dictionaries with name, progress, objective
    """
    conn = duckdb.connect()
    query = f"""
    SELECT 
        quest.name,
        quest.progress,
        quest.objective
    FROM (
        SELECT unnest(quests.active) as quest 
        FROM read_json('{filepath}')
    )
    """
    result = conn.execute(query).fetchall()
    conn.close()
    return [{"name": r[0], "progress": r[1], "objective": r[2]} for r in result]


def get_completed_quests(filepath: str) -> List[str]:
    """
    Get list of completed quest names.
    
    Args:
        filepath: Path to JSON save file
        
    Returns:
        List of completed quest names
    """
    conn = duckdb.connect()
    query = f"""
    SELECT unnest(quests.completed) as quest_name
    FROM read_json('{filepath}')
    """
    result = [r[0] for r in conn.execute(query).fetchall()]
    conn.close()
    return result


def get_playtime(filepath: str) -> float:
    """
    Get total playtime in hours.
    
    Args:
        filepath: Path to JSON save file
        
    Returns:
        Playtime in hours
    """
    conn = duckdb.connect()
    query = f"SELECT playtime_hours FROM read_json('{filepath}')"
    result = conn.execute(query).fetchone()[0]
    conn.close()
    return result


def get_achievements(filepath: str) -> List[str]:
    """
    Get list of unlocked achievements.
    
    Args:
        filepath: Path to JSON save file
        
    Returns:
        List of achievement names
    """
    conn = duckdb.connect()
    query = f"""
    SELECT unnest(achievements) as achievement
    FROM read_json('{filepath}')
    """
    result = [r[0] for r in conn.execute(query).fetchall()]
    conn.close()
    return result


if __name__ == "__main__":
    import os
    filepath = os.path.join(os.path.dirname(__file__), "..", "..", "inputs", "game_save.json")
    
    print("Player Info:")
    info = get_player_info(filepath)
    for k, v in info.items():
        print(f"  {k}: {v}")
    
    print("\nEquipped Items:")
    for item in get_equipped_items(filepath):
        print(f"  - {item}")
    
    print("\nActive Quests:")
    for quest in get_active_quests(filepath):
        print(f"  - {quest['name']}: {quest['progress']}%")
