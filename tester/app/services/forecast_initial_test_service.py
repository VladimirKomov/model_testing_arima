from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.forecast_test_result import ForecastTestResult
from app.schemas.request_schema import ForecastInitialRequest
from app.services.helpers.db_fetcher import DBFetcher
from app.services.helpers.request_sender import RequestSender
from app.utils.save_to_excel import ForecastResultSaver


class ForecastTestServiceInitialLaunch:
    def __init__(self, forward_url: str):
        self.forward_url = forward_url

    async def run(self, request_data: ForecastInitialRequest, db: AsyncSession):
        sender = RequestSender(self.forward_url)
        fetcher = DBFetcher(db)
        result_saver = ForecastResultSaver()

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
        result_saver.save(
            result=db_data,
            prefix=pref
        )

        return {
            "status": "completed",
            "item_ids": item_ids
        }
