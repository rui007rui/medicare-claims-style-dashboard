
SELECT
    COUNT(*) AS total_rows,
    COUNT(DISTINCT YEAR) AS number_of_years,
    COUNT(DISTINCT STATE) AS number_of_states
FROM ma_geo
