from app.services.helpers.request_sender import RequestSender
from app.services.helpers.db_fetcher import DBFetcher
from app.services.repositories.forecast_result_repository import ForecastResultRepository
from app.schemas.request_schema import ForecastRequest
from sqlalchemy.ext.asyncio import AsyncSession

class ForecastTestService:
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

        # # 2. Make requests to the database
        # db_data = await fetcher.fetch_data()
        #
        # # 3. Changing parameters in the database
        # await repository.save(db_data)

        #return {"status": "completed", "data": db_data}
        return {"status": "completed"}
