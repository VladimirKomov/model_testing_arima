from app.models.forecast_result import ForecastResult
from app.core.logger import logger
from sqlalchemy.ext.asyncio import AsyncSession

class ForecastResultRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def save(self, result_data: dict):
        logger.info("Сохраняем результат в БД...")
        try:
            new_entry = ForecastResult(result=result_data)
            self.db.add(new_entry)
            await self.db.commit()
            logger.success("Результат успешно сохранён")
        except Exception as e:
            logger.error(f"Ошибка при сохранении: {e}")
