import datetime
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.core.decorators import log_execution
from app.core.logger import logger
from app.schemas.forecast_test_result import ForecastTestResult
import os

def load_query(file_name: str) -> str:
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    query_path = os.path.join(base_dir, "queries", file_name)
    if not os.path.exists(query_path):
        raise FileNotFoundError(f"Query file '{file_name}' not found at '{query_path}'")
    with open(query_path, "r", encoding="utf-8") as file:
        return file.read()

class DBFetcher:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def _fetch_all_as_dicts(self, query: str, params: dict) -> list[dict]:
        """Execute the query and return the result as a list of dictionaries."""
        result = await self.db.execute(text(query), params)
        return [dict(row) for row in result.mappings().all()]

    @log_execution
    async def fetch_data(
            self,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            segment_id: Optional[int] = None,
    ) -> ForecastTestResult:
        logger.info("Starting database fetching...")

        # Set default values if they are not passed
        if start_date is None:
            start_date = datetime.date(2025, 2, 1)
        elif isinstance(start_date, str):
            start_date = datetime.date.fromisoformat(start_date)

        if end_date is None:
            end_date = datetime.date(2025, 3, 31)
        elif isinstance(end_date, str):
            end_date = datetime.date.fromisoformat(end_date)

        if segment_id is None:
            segment_id = 2

        # 1. Overall query
        forecast_overall = await self._fetch_all_as_dicts(
            load_query("forecast_overall_query.sql"),
            {
                "start_date": start_date,
                "end_date": end_date,
                "segment_id": segment_id,
            }
        )

        # 2. Топ offenders
        top_offenders = await self._fetch_all_as_dicts(
            load_query("forecast_top_offenders_query.sql"),
            {
                "start_date": start_date,
                "end_date": end_date,
                "segment_id": segment_id,
            }
        )

        # 3. Detail by offenders
        item_ids = tuple(offender["item"] for offender in top_offenders)

        top_offenders_details = await self._fetch_all_as_dicts(
            load_query("forecast_top_offenders_detail_query.sql"),
            {
                "segment_id": segment_id,
                "item_ids": item_ids,
            }
        )

        logger.success("Database fetching completed!")

        return ForecastTestResult(
            forecast_overall=forecast_overall,
            top_offenders=top_offenders,
            top_offenders_details=top_offenders_details,
        )
