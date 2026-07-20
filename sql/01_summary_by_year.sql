
SELECT
    YEAR,
    COUNT(*) AS row_count,
    SUM(BENES_MA_CNT) AS total_ma_benes,
    AVG(BENE_AVG_AGE) AS avg_age,
    AVG(ER_VISITS_PER_1000_BENES) AS avg_er_visits_per_1000,
    AVG(OP_VISITS_PER_1000_BENES) AS avg_op_visits_per_1000
FROM ma_geo
GROUP BY YEAR
ORDER BY YEAR
