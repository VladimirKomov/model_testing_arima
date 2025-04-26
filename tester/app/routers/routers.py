from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.decorators import log_execution
from app.core.logger import logger
from app.core.config import config
from app.databases.postgresql import get_db
from app.schemas.request_schema import ForecastRequest
from app.services.forecast_test_service import ForecastTestServiceInitialLaunch


router = APIRouter()


service = ForecastTestServiceInitialLaunch(
    forward_url=config.FORWARD_URL,
)


@router.post("/run-tests")
@log_execution
async def run_forecast_test(
        request_data: ForecastRequest,
        db: AsyncSession = Depends(get_db)
):
    logger.info(f"Received forecast request: {request_data}")
    return await service.run(request_data, db)
