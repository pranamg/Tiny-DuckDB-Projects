"""Chapter 14: Treasure Hunt - Solution."""
import duckdb
from typing import List, Dict, Any, Tuple


def setup_spatial(conn: duckdb.DuckDBPyConnection) -> None:
    """Install and load the spatial extension."""
    conn.execute("INSTALL spatial")
    conn.execute("LOAD spatial")


def create_treasures_table(conn: duckdb.DuckDBPyConnection) -> None:
    """Create the treasures table with spatial geometry."""
    conn.execute("""
        CREATE OR REPLACE TABLE treasures (
            id INTEGER,
            name VARCHAR,
            location GEOMETRY,
            value INTEGER
        )
    """)


def add_treasure(
    conn: duckdb.DuckDBPyConnection,
    id: int,
    name: str,
    x: float,
    y: float,
    value: int
) -> None:
    """Add a treasure at the specified location."""
    conn.execute(
        "INSERT INTO treasures VALUES (?, ?, ST_Point(?, ?), ?)",
        [id, name, x, y, value]
    )


def find_treasures_nearby(
    conn: duckdb.DuckDBPyConnection,
    player_x: float,
    player_y: float,
    radius: float
) -> List[Dict[str, Any]]:
    """
    Find all treasures within radius of player position.
    
    Args:
        conn: Database connection
        player_x: Player X coordinate
        player_y: Player Y coordinate
        radius: Search radius
        
    Returns:
        List of treasure dictionaries with name, value, distance
    """
    query = """
    SELECT 
        name,
        value,
        ST_Distance(location, ST_Point(?, ?)) as distance
    FROM treasures
    WHERE ST_DWithin(location, ST_Point(?, ?), ?)
    ORDER BY distance
    """
    result = conn.execute(query, [player_x, player_y, player_x, player_y, radius]).fetchall()
    return [{"name": r[0], "value": r[1], "distance": round(r[2], 2)} for r in result]


def find_nearest_treasure(
    conn: duckdb.DuckDBPyConnection,
    player_x: float,
    player_y: float
) -> Dict[str, Any]:
    """
    Find the nearest treasure to player position.
    
    Args:
        conn: Database connection
        player_x: Player X coordinate
        player_y: Player Y coordinate
        
    Returns:
        Dictionary with nearest treasure info
    """
    query = """
    SELECT 
        name,
        value,
        ST_Distance(location, ST_Point(?, ?)) as distance,
        ST_X(location) as x,
        ST_Y(location) as y
    FROM treasures
    ORDER BY distance
    LIMIT 1
    """
    result = conn.execute(query, [player_x, player_y]).fetchone()
    if result:
        return {
            "name": result[0],
            "value": result[1],
            "distance": round(result[2], 2),
            "x": result[3],
            "y": result[4]
        }
    return None


def calculate_total_value_in_area(
    conn: duckdb.DuckDBPyConnection,
    center_x: float,
    center_y: float,
    radius: float
) -> int:
    """
    Calculate total value of treasures in an area.
    
    Args:
        conn: Database connection
        center_x: Center X coordinate
        center_y: Center Y coordinate
        radius: Search radius
        
    Returns:
        Total value of treasures in area
    """
    query = """
    SELECT COALESCE(SUM(value), 0)
    FROM treasures
    WHERE ST_DWithin(location, ST_Point(?, ?), ?)
    """
    result = conn.execute(query, [center_x, center_y, radius]).fetchone()[0]
    return result


def get_treasure_locations(conn: duckdb.DuckDBPyConnection) -> List[Dict[str, Any]]:
    """Get all treasure locations as coordinates."""
    query = """
    SELECT 
        id, name, value,
        ST_X(location) as x,
        ST_Y(location) as y
    FROM treasures
    ORDER BY id
    """
    result = conn.execute(query).fetchall()
    return [{"id": r[0], "name": r[1], "value": r[2], "x": r[3], "y": r[4]} for r in result]


if __name__ == "__main__":
    conn = duckdb.connect()
    setup_spatial(conn)
    create_treasures_table(conn)
    
    # Add treasures
    treasures = [
        (1, "Golden Chest", 10.5, 20.3, 1000),
        (2, "Silver Coins", 15.2, 18.7, 500),
        (3, "Ancient Artifact", 8.1, 25.4, 2500),
        (4, "Gem Pouch", 12.0, 22.0, 750),
        (5, "Pirate Map", 50.0, 50.0, 100),
    ]
    for t in treasures:
        add_treasure(conn, *t)
    
    player_x, player_y = 10.0, 20.0
    print(f"Player at ({player_x}, {player_y})")
    
    print("\nTreasures within 10 units:")
    for t in find_treasures_nearby(conn, player_x, player_y, 10.0):
        print(f"  {t['name']}: {t['distance']} units away (value: {t['value']})")
    
    print("\nNearest treasure:")
    nearest = find_nearest_treasure(conn, player_x, player_y)
    if nearest:
        print(f"  {nearest['name']} at ({nearest['x']}, {nearest['y']})")
    
    conn.close()
