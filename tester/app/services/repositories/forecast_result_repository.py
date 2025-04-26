from typing import List

from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger
from app.models.forecast_result import ForecastSegmentModelParameter
from app.schemas.request_schema import ParameterUpdate


class ForecastResultRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def backup_parameters(self, updates: List[ParameterUpdate]) -> List[ParameterUpdate]:
        """Backup current parameter values before applying updates."""
        logger.info("Getting parameters before saving...")
        backup = []
        for update_item in updates:
            query = select(ForecastSegmentModelParameter).where(
                ForecastSegmentModelParameter.forecast_segment_model_id == update_item.forecast_segment_model_id,
                ForecastSegmentModelParameter.parameter_id == update_item.parameter_id
            )
            result = await self.db.execute(query)
            record = result.scalar_one_or_none()

            if record:
                backup.append(ParameterUpdate(
                    forecast_segment_model_id=record.forecast_segment_model_id,
                    parameter_id=record.parameter_id,
                    new_value=record.value  # original value
                ))
        logger.success("Parameters retrieved successfully.")
        return backup

    async def apply_parameter_updates(self, updates: List[ParameterUpdate]) -> None:
        """Apply new parameter values to the database."""
        logger.info("Saving the results in the database...")
        for update_item in updates:
            update_stmt = (
                update(ForecastSegmentModelParameter)
                .where(
                    ForecastSegmentModelParameter.forecast_segment_model_id == update_item.forecast_segment_model_id,
                    ForecastSegmentModelParameter.parameter_id == update_item.parameter_id
                )
                .values(value=update_item.new_value)
            )
            await self.db.execute(update_stmt)
        await self.db.commit()
        logger.success("Saved successfully.")

    async def revert_parameter_updates(self, backup: List[ParameterUpdate]) -> None:
        """Revert parameter values back to their original state."""
        logger.info("Reverting parameters to their original values...")
        for backup_item in backup:
            revert_stmt = (
                update(ForecastSegmentModelParameter)
                .where(
                    ForecastSegmentModelParameter.forecast_segment_model_id == backup_item.forecast_segment_model_id,
                    ForecastSegmentModelParameter.parameter_id == backup_item.parameter_id
                )
                .values(value=backup_item.new_value)
            )
            await self.db.execute(revert_stmt)
        await self.db.commit()
        logger.success("Parameters reverted successfully.")
