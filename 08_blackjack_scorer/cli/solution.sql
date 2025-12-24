-- Chapter 08: Blackjack Scorer - Solution
-- Calculate blackjack hand scores

WITH card_values AS (
    SELECT * FROM (VALUES
        ('A', 11), ('2', 2), ('3', 3), ('4', 4), ('5', 5),
        ('6', 6), ('7', 7), ('8', 8), ('9', 9), ('10', 10),
        ('J', 10), ('Q', 10), ('K', 10)
    ) AS t(rank, value)
),
hand AS (
    SELECT unnest(['AS', 'KH']) as card  -- Ace of Spades, King of Hearts
),
parsed_hand AS (
    SELECT 
        card,
        CASE 
            WHEN length(card) = 3 THEN card[1:2]
            ELSE card[1]
        END as rank
    FROM hand
),
scored AS (
    SELECT 
        p.card,
        p.rank,
        c.value,
        SUM(c.value) OVER () as total,
        SUM(CASE WHEN p.rank = 'A' THEN 1 ELSE 0 END) OVER () as ace_count
    FROM parsed_hand p
    JOIN card_values c ON p.rank = c.rank
)
SELECT 
    list(card) as hand,
    CASE 
        WHEN MAX(total) <= 21 THEN MAX(total)
        WHEN MAX(total) > 21 AND MAX(ace_count) > 0 
            THEN MAX(total) - (10 * LEAST(MAX(ace_count), (MAX(total) - 21 + 9) / 10))
        ELSE MAX(total)
    END as score,
    CASE 
        WHEN MAX(total) = 21 AND COUNT(*) = 2 THEN 'BLACKJACK!'
        WHEN MAX(total) <= 21 THEN 'OK'
        WHEN MAX(total) > 21 AND MAX(ace_count) > 0 
            AND MAX(total) - (10 * MAX(ace_count)) <= 21 THEN 'OK'
        ELSE 'BUST'
    END as status
FROM scored;
