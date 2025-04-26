from sqlalchemy.ext.asyncio import AsyncSession

from app.core.logger import logger
from app.schemas.request_schema import ForecastTestRunRequest
from app.services.helpers.db_fetcher import DBFetcher
from app.services.helpers.request_sender import RequestSender
from app.services.repositories.forecast_result_repository import ForecastResultRepository
from app.utils.save_to_excel import save_forecast_test_result_to_excel


class ForecastTestServiceMultiRun:
    def __init__(self, forward_url: str):
        self.forward_url = forward_url

    async def run(self, request_data: ForecastTestRunRequest, db: AsyncSession):
        sender = RequestSender(self.forward_url)
        fetcher = DBFetcher(db)
        repository = ForecastResultRepository(db)

        test_results = []

        for idx, parameter_updates in enumerate(request_data.parameter_update_sets, start=1):
            logger.info(f"Starting test #{idx} with {len(parameter_updates)} parameter changes.")

            # 1. Backup original parameter values
            backup_parameters = await repository.backup_parameters(parameter_updates)

            # 2. Apply new parameter updates
            await repository.apply_parameter_updates(parameter_updates)

            try:
                # 3. Send forecast request
                response = await sender.send({
                    "body": request_data.body.model_dump()
                })

                if "error" in response:
                    logger.error(f"Error during forecast request at test #{idx}: {response}")
                    test_results.append({
                        "test_number": idx,
                        "status": "error",
                        "error": response
                    })
                    continue

                # 4. Fetch test run results
                db_data = await fetcher.fetch_test_run_data(
                    item_ids=request_data.item_ids
                )

                # 5. Save results to Excel
                prefix = f'test_run_results_{idx}'
                save_path = save_forecast_test_result_to_excel(db_data, prefix=prefix)

                logger.success(f"Test #{idx} completed successfully. Result saved at {save_path}")

                test_results.append({
                    "test_number": idx,
                    "status": "completed",
                    "file_path": save_path,
                    "item_ids": request_data.item_ids
                })

            finally:
                # 6. Revert original parameters
                await repository.revert_parameter_updates(backup_parameters)
                logger.info(f"Parameters reverted after test #{idx}.")

        return {
            "summary": test_results
        }
