from sys import prefix

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.forecast_test_result import ForecastTestResult
from app.schemas.request_schema import ForecastInitialRequest
from app.services.helpers.db_fetcher import DBFetcher
from app.services.helpers.request_sender import RequestSender
from app.services.repositories.forecast_result_repository import ForecastResultRepository
from app.utils.save_to_excel import save_forecast_test_result_to_excel


class ForecastTestServiceInitialLaunch:
    def __init__(self, forward_url: str):
        self.forward_url = forward_url

    async def run(self, request_data: ForecastInitialRequest, db: AsyncSession):
        sender = RequestSender(self.forward_url)
        fetcher = DBFetcher(db)
        repository = ForecastResultRepository(db)

        # 1. Sending a request
        response = await sender.send(request_data.model_dump())

        if "error" in response:
            return response

        # 2. Make requests to the database
        db_data: ForecastTestResult
        item_ids: list[int]
        db_data, item_ids = await fetcher.fetch_initial_data()

        # 3. Save to Excel in a separate folder
        pref = 'initial_test_results'
        save_forecast_test_result_to_excel(db_data, prefix=pref)

        return {
            "status": "completed",
            "item_ids": item_ids
        }
