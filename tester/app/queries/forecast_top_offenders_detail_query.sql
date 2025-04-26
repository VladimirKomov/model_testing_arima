--Data Per Comb-----------------------------------------------------------------------------------------------------------

SELECT s.ITEM_ID ITEM, s.ITEM, s.SALES_DATE DATE,
       SUM(s.final_history) HISTORY,

-- SUM(COALESCE(s.demand_forecast_1, 0)) SEASONAL_ARIMA_FORECAST,
       SUM(COALESCE(s.demand_forecast_2, 0)) AUTO_ARIMA_FORECAST
-- SUM(COALESCE(s.FINAL_FORECAST, 0)) DEMANTRA_FORECAST
FROM ds_matrix m,
     ds_data s
-- (SELECT MAX(DATA_ID) AS ID, MAX(T1.ITEM_ID) AS ITEM_ID, MAX(T1.ITEM) AS ITEM, MAX(T1.LOCATION_ID) AS LOCATION_ID, MAX(T1.ORGANIZATION) AS ORGANIZATION,
-- 		MAX(T1.SALES_DATE) AS SALES_DATE, SUM(FINAL_HISTORY) AS FINAL_HISTORY, SUM(FINAL_FORECAST) AS FINAL_FORECAST, SUM(DEMAND_FORECAST_1) AS DEMAND_FORECAST_1, SUM(DEMAND_FORECAST_2) AS DEMAND_FORECAST_2
-- 	FROM
-- 		(SELECT DATA.ID AS DATA_ID, DATA., CAL.
-- 		FROM public.ds_data AS DATA
-- 		JOIN public.calendar AS CAL ON CAL.date = DATA.sales_date) AS T1
-- 		LEFT JOIN public.ds_correlation_factor AS DS
-- 		ON T1.location_id = DS.location_id
-- 		WHERE SALES_DATE >= (SELECT min(date) as date
-- 							FROM public.calendar
-- 							WHERE AGGREGATION_1 = (SELECT AGGREGATION_1
-- 													FROM public.calendar
-- 													WHERE date = '2021-01-01'))
-- 		AND SALES_DATE <= '2026-08-31'
-- 		GROUP BY T1.Item_id,T1.Location_id, T1.AGGREGATION_1) s
WHERE s.ITEM_ID = m.ITEM_ID
  AND s.LOCATION_ID = m.LOCATION_ID
  AND s.SALES_DATE >= '2021-11-29'
  AND s.SALES_DATE <= '2026-08-31'
  AND m.SEGMENT_DEM_ID = :segment_id
  AND s.item_id = ANY(:item_ids)
  and s.location_id = 3
GROUP BY s.ITEM_ID, S.ITEM, s.LOCATION_ID, s.SALES_DATE
ORDER BY s.ITEM_ID, s.LOCATION_ID, s.SALES_DATE