import datetime
import os
from typing import Optional, Sequence

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.decorators import log_execution
from app.core.logger import logger
from app.schemas.forecast_test_result import ForecastTestResult


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

    async def _fetch_forecast_overall(self, start_date: datetime.date, end_date: datetime.date, segment_id: int) -> \
            list[dict]:
        query = load_query("forecast_overall_query.sql")
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "segment_id": segment_id,
        }
        return await self._fetch_all_as_dicts(query, params)

    async def _fetch_top_offenders(self, start_date: datetime.date, end_date: datetime.date, segment_id: int) -> list[
        dict]:
        query = load_query("forecast_top_offenders_query.sql")
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "segment_id": segment_id,
        }
        return await self._fetch_all_as_dicts(query, params)

    async def _fetch_top_offenders_details(self, segment_id: int, item_ids: Sequence[int]) -> list[dict]:
        query = load_query("forecast_top_offenders_detail_query.sql")
        params = {
            "segment_id": segment_id,
            "item_ids": item_ids,
        }
        return await self._fetch_all_as_dicts(query, params)

    def _ensure_dates(
            self,
            start_date: Optional[str],
            end_date: Optional[str],
            segment_id: Optional[int]
    ) -> tuple[datetime.date, datetime.date, int]:
        """Ensure that dates are valid datetime.date and segment_id is int."""

        def parse_date(value: Optional[str], default: datetime.date) -> datetime.date:
            if value is None:
                return default
            if isinstance(value, datetime.date):
                return value
            try:
                return datetime.date.fromisoformat(value)
            except ValueError:
                raise ValueError(f"Invalid date format: '{value}'. Expected format 'YYYY-MM-DD'.")

        start_date = parse_date(start_date, datetime.date(2025, 2, 1))
        end_date = parse_date(end_date, datetime.date(2025, 3, 31))
        segment_id = segment_id if segment_id is not None else 0

        return start_date, end_date, segment_id

    @log_execution
    async def fetch_initial_data(
            self,
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            segment_id: Optional[int] = None,
    ) -> tuple[ForecastTestResult, list[int]]:
        logger.info("Starting database fetching...")

        start_date, end_date, segment_id = self._ensure_dates(start_date, end_date, segment_id)

        forecast_overall = await self._fetch_forecast_overall(start_date, end_date, segment_id)
        top_offenders = await self._fetch_top_offenders(start_date, end_date, segment_id)

        item_ids = tuple(int(offender["item"]) for offender in top_offenders)

        top_offenders_details = await self._fetch_top_offenders_details(segment_id, item_ids)

        logger.success("Database fetching completed!")

        forecast_test_result = ForecastTestResult(
            forecast_overall=forecast_overall,
            top_offenders=top_offenders,
            top_offenders_details=top_offenders_details,
        )

        return forecast_test_result, list(item_ids)

    @log_execution
    async def fetch_test_run_data(
            self,
            item_ids: list[int],
            start_date: Optional[str] = None,
            end_date: Optional[str] = None,
            segment_id: Optional[int] = None,
    ) -> ForecastTestResult:
        """Fetch forecast_overall and top_offenders_details for given item_ids."""
        logger.info("Starting test run data fetching...")

        start_date, end_date, segment_id = self._ensure_dates(start_date, end_date, segment_id)

        # Fetch overall forecast
        forecast_overall = await self._fetch_forecast_overall(start_date, end_date, segment_id)

        # Fetch top offenders details only for provided item_ids
        top_offenders_details = await self._fetch_top_offenders_details(segment_id, item_ids)

        logger.success("Test run data fetching completed!")

        return ForecastTestResult(
            forecast_overall=forecast_overall,
            # We skip top_offenders in this case
            top_offenders=[],
            top_offenders_details=top_offenders_details,
        )
