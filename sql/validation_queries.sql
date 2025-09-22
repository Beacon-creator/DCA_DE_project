-- Row count
SELECT COUNT(*) AS total_rows FROM netflix_titles_table;

-- Null checks
SELECT 
    SUM(CASE WHEN show_id IS NULL THEN 1 ELSE 0 END) AS null_show_id,
    SUM(CASE WHEN title IS NULL THEN 1 ELSE 0 END) AS null_title,
    SUM(CASE WHEN type IS NULL THEN 1 ELSE 0 END) AS null_type
FROM netflix_titles_table;

-- Duplicate check
SELECT show_id, COUNT(*) AS occurrences
FROM netflix_titles_table
GROUP BY show_id
HAVING COUNT(*) > 1;
