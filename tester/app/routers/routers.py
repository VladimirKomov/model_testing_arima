from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.decorators import log_execution
from app.core.logger import logger
from app.core.config import config
from app.databases.postgresql import get_db
from app.schemas.request_schema import ForecastInitialRequest, ForecastTestRunRequest
from app.services.forecast_initial_test_service import ForecastTestServiceInitialLaunch
from app.services.forecast_test_service_multi_run import ForecastTestServiceMultiRun

router = APIRouter()


@router.post("/run-initial-test")
@log_execution
async def run_forecast_test(
        request_data: ForecastInitialRequest,
        db: AsyncSession = Depends(get_db)
):
    logger.info(f"Received initial request: {request_data}")
    initial_service = ForecastTestServiceInitialLaunch(
        forward_url=config.FORWARD_URL,
    )
    return await initial_service.run(request_data, db)


@router.post("/run-multi-test")
@log_execution
async def run_multi_test(
        request_data: ForecastTestRunRequest,
        db: AsyncSession = Depends(get_db)
):
    logger.info(f"Received multi-test request: {request_data}")
    service = ForecastTestServiceMultiRun(
        forward_url=config.FORWARD_URL
    )
    return await service.run(request_data, db)
