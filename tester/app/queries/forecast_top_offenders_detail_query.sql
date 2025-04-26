--========================================
-- EMERSON Weekly Forecast
-- Top Offenders Detailed View by Item and Date
--========================================

SELECT
    s.ITEM_ID AS ITEM_ID,
    s.ITEM AS ITEM_NAME,
    s.SALES_DATE AS DATE,
    SUM(s.final_history) AS HISTORY,
    SUM(COALESCE(s.demand_forecast_2, 0)) AS AUTO_ARIMA_FORECAST
FROM
    ds_matrix m
    JOIN
    ds_data s ON s.ITEM_ID = m.ITEM_ID AND s.LOCATION_ID = m.LOCATION_ID
WHERE
    s.SALES_DATE >= :start_date
  AND s.SALES_DATE <= :end_date
  AND m.SEGMENT_DEM_ID = :segment_id
  AND s.item_id IN :item_ids
  AND s.location_id = :location_id
GROUP BY
    s.ITEM_ID,
    s.ITEM,
    s.LOCATION_ID,
    s.SALES_DATE
ORDER BY
    s.ITEM_ID,
    s.LOCATION_ID,
    s.SALES_DATE;
