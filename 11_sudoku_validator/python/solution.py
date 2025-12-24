"""Chapter 11: Sudoku Validator - Solution."""
import duckdb
from typing import List, Tuple


def create_board_table(conn: duckdb.DuckDBPyConnection, board: List[List[int]]) -> None:
    """Create a temp table with the sudoku board."""
    conn.execute("DROP TABLE IF EXISTS sudoku")
    conn.execute("""
        CREATE TEMP TABLE sudoku (
            row_num INTEGER,
            c1 INTEGER, c2 INTEGER, c3 INTEGER,
            c4 INTEGER, c5 INTEGER, c6 INTEGER,
            c7 INTEGER, c8 INTEGER, c9 INTEGER
        )
    """)
    for i, row in enumerate(board):
        conn.execute(
            "INSERT INTO sudoku VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [i + 1] + row
        )


def validate_rows(conn: duckdb.DuckDBPyConnection) -> bool:
    """Check that each row contains 1-9 exactly once."""
    query = """
    WITH cells AS (
        SELECT row_num, unnest([c1,c2,c3,c4,c5,c6,c7,c8,c9]) as val FROM sudoku
    ),
    row_counts AS (
        SELECT row_num, COUNT(DISTINCT val) as cnt
        FROM cells
        GROUP BY row_num
    )
    SELECT bool_and(cnt = 9) FROM row_counts
    """
    result = conn.execute(query).fetchone()
    return result[0] if result else False


def validate_columns(conn: duckdb.DuckDBPyConnection) -> bool:
    """Check that each column contains 1-9 exactly once."""
    query = """
    WITH cells AS (
        SELECT row_num, 1 as col_num, c1 as val FROM sudoku
        UNION ALL SELECT row_num, 2, c2 FROM sudoku
        UNION ALL SELECT row_num, 3, c3 FROM sudoku
        UNION ALL SELECT row_num, 4, c4 FROM sudoku
        UNION ALL SELECT row_num, 5, c5 FROM sudoku
        UNION ALL SELECT row_num, 6, c6 FROM sudoku
        UNION ALL SELECT row_num, 7, c7 FROM sudoku
        UNION ALL SELECT row_num, 8, c8 FROM sudoku
        UNION ALL SELECT row_num, 9, c9 FROM sudoku
    )
    SELECT bool_and(cnt = 9)
    FROM (
        SELECT col_num, COUNT(DISTINCT val) as cnt
        FROM cells
        GROUP BY col_num
    )
    """
    result = conn.execute(query).fetchone()
    return result[0] if result else False


def validate_boxes(conn: duckdb.DuckDBPyConnection) -> bool:
    """Check that each 3x3 box contains 1-9 exactly once."""
    query = """
    WITH cells AS (
        SELECT row_num, 1 as col_num, c1 as val FROM sudoku
        UNION ALL SELECT row_num, 2, c2 FROM sudoku
        UNION ALL SELECT row_num, 3, c3 FROM sudoku
        UNION ALL SELECT row_num, 4, c4 FROM sudoku
        UNION ALL SELECT row_num, 5, c5 FROM sudoku
        UNION ALL SELECT row_num, 6, c6 FROM sudoku
        UNION ALL SELECT row_num, 7, c7 FROM sudoku
        UNION ALL SELECT row_num, 8, c8 FROM sudoku
        UNION ALL SELECT row_num, 9, c9 FROM sudoku
    )
    SELECT bool_and(cnt = 9)
    FROM (
        SELECT 
            ((row_num - 1) // 3) as box_row,
            ((col_num - 1) // 3) as box_col,
            COUNT(DISTINCT val) as cnt
        FROM cells
        GROUP BY box_row, box_col
    )
    """
    result = conn.execute(query).fetchone()
    return result[0] if result else False


def validate_board(board: List[List[int]]) -> dict:
    """
    Validate a complete sudoku board.
    
    Args:
        board: 9x9 list of integers
        
    Returns:
        Dictionary with rows_valid, cols_valid, boxes_valid, is_valid
    """
    conn = duckdb.connect()
    create_board_table(conn, board)
    
    rows = validate_rows(conn)
    cols = validate_columns(conn)
    boxes = validate_boxes(conn)
    
    conn.close()
    
    return {
        "rows_valid": rows,
        "cols_valid": cols,
        "boxes_valid": boxes,
        "is_valid": rows and cols and boxes
    }


def get_invalid_cells(board: List[List[int]]) -> List[Tuple[int, int, str]]:
    """
    Find cells that violate sudoku rules.
    
    Args:
        board: 9x9 list of integers
        
    Returns:
        List of (row, col, reason) tuples
    """
    conn = duckdb.connect()
    create_board_table(conn, board)
    
    query = """
    WITH cells AS (
        SELECT row_num, 1 as col_num, c1 as val FROM sudoku
        UNION ALL SELECT row_num, 2, c2 FROM sudoku
        UNION ALL SELECT row_num, 3, c3 FROM sudoku
        UNION ALL SELECT row_num, 4, c4 FROM sudoku
        UNION ALL SELECT row_num, 5, c5 FROM sudoku
        UNION ALL SELECT row_num, 6, c6 FROM sudoku
        UNION ALL SELECT row_num, 7, c7 FROM sudoku
        UNION ALL SELECT row_num, 8, c8 FROM sudoku
        UNION ALL SELECT row_num, 9, c9 FROM sudoku
    ),
    row_dups AS (
        SELECT row_num, val, COUNT(*) as cnt
        FROM cells GROUP BY row_num, val HAVING cnt > 1
    ),
    col_dups AS (
        SELECT col_num, val, COUNT(*) as cnt
        FROM cells GROUP BY col_num, val HAVING cnt > 1
    )
    SELECT DISTINCT c.row_num, c.col_num, 'duplicate in row' as reason
    FROM cells c JOIN row_dups r ON c.row_num = r.row_num AND c.val = r.val
    UNION
    SELECT DISTINCT c.row_num, c.col_num, 'duplicate in column'
    FROM cells c JOIN col_dups d ON c.col_num = d.col_num AND c.val = d.val
    """
    result = conn.execute(query).fetchall()
    conn.close()
    return result


# Sample valid board
VALID_BOARD = [
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9]
]

# Sample invalid board (duplicate 5 in first row)
INVALID_BOARD = [
    [5, 3, 5, 6, 7, 8, 9, 1, 2],  # Two 5s in row 1
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9]
]


if __name__ == "__main__":
    print("Validating valid board:")
    result = validate_board(VALID_BOARD)
    print(f"  {result}")
    
    print("\nValidating invalid board:")
    result = validate_board(INVALID_BOARD)
    print(f"  {result}")
