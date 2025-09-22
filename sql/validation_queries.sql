-- Example queries

-- Count movies vs TV shows
SELECT type, COUNT(*) FROM movies GROUP BY type;

-- Most common rating
SELECT rating, COUNT(*) FROM movies GROUP BY rating ORDER BY COUNT(*) DESC;

-- Top directors with most content
SELECT director, COUNT(*) FROM movies GROUP BY director ORDER BY COUNT(*) DESC LIMIT 10;
