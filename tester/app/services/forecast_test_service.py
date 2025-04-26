import os
from datetime import datetime

from app.schemas.forecast_test_result import ForecastTestResult
from app.services.helpers.request_sender import RequestSender
from app.services.helpers.db_fetcher import DBFetcher
from app.services.repositories.forecast_result_repository import ForecastResultRepository
from app.schemas.request_schema import ForecastRequest
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.save_to_excel import save_forecast_test_result_to_excel


class ForecastTestServiceInitialLaunch:
    def __init__(self, forward_url: str):
        self.forward_url = forward_url

    async def run(self, request_data: ForecastRequest, db: AsyncSession):
        sender = RequestSender(self.forward_url)
        fetcher = DBFetcher(db)
        repository = ForecastResultRepository(db)

        # 1. Sending a request
        response = await sender.send(request_data.model_dump())

        if "error" in response:
            return response

        # 2. Make requests to the database
        db_data: ForecastTestResult = await fetcher.fetch_data()

        # 3. Save to Excel in a separate folder
        save_forecast_test_result_to_excel(db_data)


        #return {"status": "completed", "data": db_data}
        return {"status": "completed"}
