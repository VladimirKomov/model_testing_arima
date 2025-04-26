--========================================
-- EMERSON Weekly Forecast
-- Top Offenders Aggregated Results
--========================================

WITH FORECAST_DATA AS (
    SELECT
        ITEM,
        LOCATION,
        SEGMENT_ID,
        PREDICTION_STATUS,
        SUM(HISTORY) AS HISTORY,
        SUM(ARIMA_FORECAST) AS ARIMA_FORECAST,
        SUM(ABS_ERROR_ARIMA) AS ARIMA_ERROR,
        SUM(XGBOOST_FORECAST) AS XGBOOST_FORECAST,
        SUM(ABS_ERROR_XGBOOST) AS XGBOOST_ERROR,
        SUM(MA_FORECAST) AS MA_FORECAST,
        SUM(ABS_ERROR_MA) AS MA_ERROR,
        SUM(BLENDED_FORECAST) AS BLENDED_FORECAST,
        SUM(ABS_ERROR_BLENDED) AS BLENDED_ERROR,
        SUM(DEMANTRA_FORECAST) AS DEMANTRA_FORECAST,
        SUM(ABS_ERROR_DEMANTRA) AS DEMANTRA_ERROR
    FROM (
             SELECT
                 MAX(T1.ITEM_ID) AS ITEM,
                 MAX(T1.LOCATION_ID) AS LOCATION,
                 MAX(SEGMENT_DEM_ID) AS SEGMENT_ID,
                 MAX(CASE WHEN DEMAND_VALID = TRUE THEN 1 ELSE 0 END) AS PREDICTION_STATUS,
                 MIN(SALES_DATE) AS DATE,
            SUM(T1.FINAL_HISTORY) AS HISTORY,
            SUM(COALESCE(T1.demand_forecast_1, 0)) AS SEASONAL_FORECAST,
            ABS(SUM(T1.FINAL_HISTORY) - SUM(COALESCE(T1.demand_forecast_1, 0))) AS ABS_ERROR_SEASONAL,
            SUM(COALESCE(T1.demand_forecast_2, 0)) AS ARIMA_FORECAST,
            ABS(SUM(T1.FINAL_HISTORY) - SUM(COALESCE(T1.demand_forecast_2, 0))) AS ABS_ERROR_ARIMA,
            SUM(COALESCE(T1.demand_forecast_3, 0)) AS XGBOOST_FORECAST,
            ABS(SUM(T1.FINAL_HISTORY) - SUM(COALESCE(T1.demand_forecast_3, 0))) AS ABS_ERROR_XGBOOST,
            SUM(COALESCE(T1.demand_forecast_4, 0)) AS MA_FORECAST,
            ABS(SUM(T1.FINAL_HISTORY) - SUM(COALESCE(T1.demand_forecast_4, 0))) AS ABS_ERROR_MA,
            SUM(COALESCE(T1.demand_forecast, 0)) AS BLENDED_FORECAST,
            ABS(SUM(T1.FINAL_HISTORY) - SUM(COALESCE(T1.demand_forecast, 0))) AS ABS_ERROR_BLENDED,
            SUM(COALESCE(T1.final_forecast, 0)) AS DEMANTRA_FORECAST,
            ABS(SUM(T1.FINAL_HISTORY) - SUM(COALESCE(T1.final_forecast, 0))) AS ABS_ERROR_DEMANTRA
             FROM (
                 SELECT
                 DATA.*,
                 CAL.*
                 FROM PUBLIC.DS_DATA AS DATA
                 JOIN PUBLIC.CALENDAR AS CAL ON CAL.DATE = DATA.SALES_DATE
                 ) AS T1
                 JOIN DS_MATRIX AS MATRIX ON
                 T1.ITEM_ID = MATRIX.ITEM_ID
                 AND T1.LOCATION_ID = MATRIX.LOCATION_ID
             WHERE SALES_DATE >= :start_date
               AND SALES_DATE <= :end_date
             GROUP BY
                 T1.ITEM_ID,
                 T1.LOCATION_ID,
                 T1.AGGREGATION_2
         ) AS subquery
    WHERE SEGMENT_ID = :segment_id
    GROUP BY
        ITEM,
        LOCATION,
        SEGMENT_ID,
        PREDICTION_STATUS
)

SELECT *
FROM (
         SELECT
             ITEM,
             LOCATION,
             SEGMENT_ID,
             PREDICTION_STATUS,
             HISTORY,
             ARIMA_FORECAST,
             ARIMA_ERROR,
             DEMANTRA_FORECAST,
             DEMANTRA_ERROR
         FROM FORECAST_DATA
         WHERE SEGMENT_ID IN (:segment_id)
         ORDER BY ARIMA_ERROR DESC -- сортируем по ошибке ARIMA
     )
         LIMIT 20;
