"""Chapter 01: Hello Duck - Solution."""
import duckdb


def hello() -> str:
    """
    Return the greeting "Hello, DuckDB!" using a DuckDB query.
    
    Returns:
        str: The greeting string
    """
    conn = duckdb.connect()
    result = conn.execute("SELECT 'Hello, DuckDB!' AS greeting").fetchone()[0]
    conn.close()
    return result


if __name__ == "__main__":
    print(hello())
