import os
import json
import datetime
from typing import Optional, List

import pandas as pd
from app.schemas.forecast_test_result import ForecastTestResult
from app.schemas.request_schema import ParameterUpdate

class ForecastResultSaver:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.base_dir = os.path.join(base_dir, "forecast_test_results")
        os.makedirs(self.base_dir, exist_ok=True)

    def _create_today_folder(self) -> str:
        """Create a folder for today's date."""
        today = datetime.datetime.now().strftime("%Y%m%d")
        today_folder = os.path.join(self.base_dir, today)
        os.makedirs(today_folder, exist_ok=True)
        return today_folder

    def save(self, result: ForecastTestResult, prefix: str, parameter_updates: Optional[List[ParameterUpdate]] = None) -> dict:
        """Save forecast results to Excel (+ optionally parameter updates to JSON)."""
        today_folder = self._create_today_folder()
        timestamp = datetime.datetime.now().strftime("%H%M%S")

        # Generate file paths
        base_name = f"{prefix}_{timestamp}"
        excel_file_path = os.path.join(today_folder, f"{base_name}.xlsx")

        # Save Excel
        data_dict = result.to_dict()
        with pd.ExcelWriter(excel_file_path, engine="openpyxl") as writer:
            for sheet_name, data in data_dict.items():
                if data:
                    df = pd.DataFrame(data)
                    df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
                else:
                    pd.DataFrame([{"info": "No data"}]).to_excel(writer, sheet_name=sheet_name[:31], index=False)

        # Prepare result dictionary
        result_paths = {
            "excel_path": excel_file_path
        }

        # Save JSON only if parameter_updates provided
        if parameter_updates:
            json_file_path = os.path.join(today_folder, f"{base_name}_params.json")
            updates_as_dict = [update.model_dump() for update in parameter_updates]
            with open(json_file_path, "w", encoding="utf-8") as f:
                json.dump(updates_as_dict, f, indent=2, ensure_ascii=False)  # type: ignore[arg-type]

            result_paths["json_path"] = json_file_path

        return result_paths
