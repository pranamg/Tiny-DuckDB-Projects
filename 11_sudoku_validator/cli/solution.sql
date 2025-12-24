-- Chapter 11: Sudoku Validator - Solution
-- Validate a completed sudoku board

-- Create a sample valid sudoku board
CREATE OR REPLACE TEMP TABLE sudoku AS
SELECT * FROM (VALUES
    (1, 5, 3, 4, 6, 7, 8, 9, 1, 2),
    (2, 6, 7, 8, 1, 9, 5, 3, 4, 2),
    (3, 1, 9, 8, 3, 4, 2, 5, 6, 7),
    (4, 8, 5, 9, 7, 6, 1, 4, 2, 3),
    (5, 4, 2, 6, 8, 5, 3, 7, 9, 1),
    (6, 7, 1, 3, 9, 2, 4, 8, 5, 6),
    (7, 9, 6, 1, 5, 3, 7, 2, 8, 4),
    (8, 2, 8, 7, 4, 1, 9, 6, 3, 5),
    (9, 3, 4, 5, 2, 8, 6, 1, 7, 9)
) AS t(row_num, c1, c2, c3, c4, c5, c6, c7, c8, c9);

-- Unpivot to get individual cells
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
-- Check rows (each row has 1-9)
row_check AS (
    SELECT row_num, COUNT(DISTINCT val) = 9 as valid
    FROM cells
    GROUP BY row_num
),
-- Check columns (each column has 1-9)
col_check AS (
    SELECT col_num, COUNT(DISTINCT val) = 9 as valid
    FROM cells
    GROUP BY col_num
),
-- Check 3x3 boxes
box_check AS (
    SELECT 
        ((row_num - 1) / 3) as box_row,
        ((col_num - 1) / 3) as box_col,
        COUNT(DISTINCT val) = 9 as valid
    FROM cells
    GROUP BY box_row, box_col
)
SELECT 
    bool_and(r.valid) as rows_valid,
    bool_and(c.valid) as cols_valid,
    bool_and(b.valid) as boxes_valid,
    bool_and(r.valid) AND bool_and(c.valid) AND bool_and(b.valid) as board_valid
FROM row_check r, col_check c, box_check b;
