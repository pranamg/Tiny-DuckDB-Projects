"""Chapter 06: Picnic Planner - Solution."""
import duckdb
from typing import List


def format_items(items: List[str]) -> str:
    """
    Format a list of items with proper grammar.
    
    Args:
        items: List of items to format
        
    Returns:
        Formatted string:
        - 1 item: "chips"
        - 2 items: "chips and dip"
        - 3+ items: "chips, dip, and salsa"
    """
    if not items:
        return ""
    
    conn = duckdb.connect()
    conn.execute("CREATE TEMP TABLE items (item VARCHAR)")
    conn.executemany("INSERT INTO items VALUES (?)", [(i,) for i in items])
    
    query = """
    WITH item_list AS (
        SELECT list(item) as all_items FROM items
    )
    SELECT 
        CASE 
            WHEN len(all_items) = 1 THEN all_items[1]
            WHEN len(all_items) = 2 THEN all_items[1] || ' and ' || all_items[2]
            ELSE array_to_string(all_items[1:-1], ', ') || ', and ' || all_items[-1]
        END
    FROM item_list
    """
    result = conn.execute(query).fetchone()[0]
    conn.close()
    return result


def format_items_with_oxford_comma(items: List[str], use_oxford: bool = True) -> str:
    """
    Format items with optional Oxford comma.
    
    Args:
        items: List of items to format
        use_oxford: Whether to use Oxford comma (default True)
        
    Returns:
        Formatted string
    """
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    if len(items) == 2:
        return f"{items[0]} and {items[1]}"
    
    conn = duckdb.connect()
    if use_oxford:
        query = """
        SELECT array_to_string(?[1:-1], ', ') || ', and ' || ?[-1]
        """
    else:
        query = """
        SELECT array_to_string(?[1:-1], ', ') || ' and ' || ?[-1]
        """
    result = conn.execute(query, [items, items]).fetchone()[0]
    conn.close()
    return result


def create_packing_list(items: List[str], quantities: List[int]) -> str:
    """
    Create a packing list with quantities.
    
    Args:
        items: List of item names
        quantities: List of quantities for each item
        
    Returns:
        Formatted packing list
    """
    conn = duckdb.connect()
    conn.execute("""
        CREATE TEMP TABLE packing (item VARCHAR, qty INTEGER)
    """)
    for item, qty in zip(items, quantities):
        conn.execute("INSERT INTO packing VALUES (?, ?)", [item, qty])
    
    query = """
    SELECT string_agg(qty || 'x ' || item, ', ' ORDER BY item)
    FROM packing
    """
    result = conn.execute(query).fetchone()[0]
    conn.close()
    return result


if __name__ == "__main__":
    print(format_items(["chips"]))
    print(format_items(["chips", "dip"]))
    print(format_items(["chips", "dip", "salsa"]))
    print(format_items(["chips", "dip", "salsa", "guacamole"]))
