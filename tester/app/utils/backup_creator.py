import os
import json
import zipfile
import datetime
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.logger import logger
from app.schemas.request_schema import ParameterUpdate

class BackupCreator:
    def __init__(self, db: AsyncSession):
        self.db = db
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.base_backup_dir = os.path.join(base_dir, "forecast_test_backups")
        os.makedirs(self.base_backup_dir, exist_ok=True)

    def _create_today_folder(self) -> str:
        """Create a subfolder for today's date."""
        today = datetime.datetime.now().strftime("%Y%m%d")
        today_folder = os.path.join(self.base_backup_dir, today)
        os.makedirs(today_folder, exist_ok=True)
        return today_folder

    async def export_ds_data(self, csv_path: str) -> bool:
        """Export the ds_data table to a CSV file."""
        logger.info("Exporting ds_data table to CSV...")
        result = await self.db.execute(text("SELECT * FROM ds_data"))
        rows = result.mappings().all()

        if not rows:
            logger.warning("No data found in ds_data table.")
            return False

        # Convert to DataFrame
        df = pd.DataFrame(rows)
        df.to_csv(csv_path, index=False)

        logger.success(f"ds_data exported successfully to {csv_path} ({len(df)} rows)")
        return True

    def save_parameter_changes(self, parameter_updates: list[ParameterUpdate], json_path: str) -> bool:
        """Save parameter updates to a JSON file."""
        logger.info("Saving parameter updates to JSON...")
        if not parameter_updates:
            logger.warning("No parameter updates provided.")
            return False

        updates_as_dict = [update.model_dump() for update in parameter_updates]
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(updates_as_dict, f, indent=2, ensure_ascii=False)

        logger.success(f"Parameter updates saved successfully to {json_path} ({len(updates_as_dict)} updates)")
        return True

    def create_backup_archive(self, files_to_archive: list[str], zip_path: str):
        """Create a zip archive with specified files."""
        logger.info("Creating backup archive...")
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file_path in files_to_archive:
                if os.path.exists(file_path):
                    zipf.write(file_path, arcname=os.path.basename(file_path))
                else:
                    logger.warning(f"File not found and skipped: {file_path}")
        logger.success(f"Backup archive created: {zip_path}")

    async def create_full_backup(self, parameter_updates: list[ParameterUpdate], test_number: int) -> str:
        """Full backup process: export ds_data, save parameter updates, archive everything."""
        today_folder = self._create_today_folder()
        timestamp = datetime.datetime.now().strftime("%H%M%S")

        csv_path = os.path.join(today_folder, f"ds_data_backup_test{test_number}_{timestamp}.csv")
        json_path = os.path.join(today_folder, f"parameter_changes_test{test_number}_{timestamp}.json")
        zip_path = os.path.join(today_folder, f"full_backup_test{test_number}_{timestamp}.zip")

        # Try exporting
        ds_data_success = await self.export_ds_data(csv_path)
        param_save_success = self.save_parameter_changes(parameter_updates, json_path)

        files_to_archive = []
        if ds_data_success:
            files_to_archive.append(csv_path)
        if param_save_success:
            files_to_archive.append(json_path)

        if files_to_archive:
            self.create_backup_archive(files_to_archive, zip_path)

            # Optionally delete temp files
            for file_path in files_to_archive:
                try:
                    os.remove(file_path)
                except Exception as e:
                    logger.warning(f"Failed to delete temp file {file_path}: {e}")

            return zip_path
        else:
            logger.error("Backup failed: No files were generated to archive.")
            return ""
