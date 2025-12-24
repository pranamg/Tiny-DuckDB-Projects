-- Chapter 12: JSON Quest - Solution
-- Parse and query game save files

-- Load the JSON file
WITH save_data AS (
    SELECT * FROM read_json('../inputs/game_save.json')
)
-- Extract player info
SELECT 
    player.name as player_name,
    player.level as level,
    player.class as class,
    player.health as current_health,
    player.max_health as max_health,
    ROUND(100.0 * player.health / player.max_health, 1) as health_pct,
    playtime_hours,
    len(achievements) as achievement_count
FROM save_data;

-- To extract inventory items, use:
-- SELECT unnest(inventory) as item FROM read_json('../inputs/game_save.json');

-- To extract active quests:
-- SELECT unnest(quests.active) as quest FROM read_json('../inputs/game_save.json');
