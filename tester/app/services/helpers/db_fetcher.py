import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.logger import logger
from app.schemas.forecast_test_result import ForecastTestResult


# Утилита для загрузки SQL-файлов
def load_query(file_name: str) -> str:
    base_dir = os.path.dirname(__file__)  # путь до db_fetcher.py
    query_path = os.path.join(base_dir, "../../../queries", file_name)
    with open(query_path, "r", encoding="utf-8") as file:
        return file.read()

class DBFetcher:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def fetch_data(self) -> ForecastTestResult:
        logger.info("Starting to make complex queries to the database...")

        # 1. forecast_data_query.sql
        forecast_data_query = load_query("forecast_data_query.sql")
        res1 = await self.db.execute(text(forecast_data_query), {
            "start_date": "2025-02-01",
            "end_date": "2025-03-31",
            "segment_id": 2
        })
        forecast_data = res1.mappings().all()

        # 2. forecast_overall_query.sql
        forecast_overall_query = load_query("forecast_overall_query.sql")
        res2 = await self.db.execute(text(forecast_overall_query))
        forecast_overall = res2.mappings().all()

        # 3. forecast_top_offenders_query.sql
        forecast_top_offenders_query = load_query("forecast_top_offenders_query.sql")
        res3 = await self.db.execute(text(forecast_top_offenders_query), {
            "start_date": "2025-02-01",
            "end_date": "2025-03-31",
            "segment_id": 2
        })
        top_offenders = res3.mappings().all()

        # 4. forecast_top_offenders_detail_query.sql
        item_ids = (78,1265,148,9926,6917,5486,11050,10019,8872,4761,1845,10742,9050,9316,4341,1488,2177,3809,5482,6950)
        location_id = 3

        forecast_top_offenders_detail_query = load_query("forecast_top_offenders_detail_query.sql")
        res4 = await self.db.execute(text(forecast_top_offenders_detail_query), {
            "start_date": "2025-02-01",
            "end_date": "2025-03-31",
            "segment_id": 2,
            "item_ids": item_ids,
            "location_id": location_id
        })
        top_offenders_details = res4.mappings().all()

        logger.success("All data collected successfully")

        return ForecastTestResult(
            forecast_data=forecast_data,
            forecast_overall=forecast_overall,
            top_offenders=top_offenders,
            top_offenders_details=top_offenders_details
        )
