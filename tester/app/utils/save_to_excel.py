import os
import pandas as pd
from datetime import datetime
from app.schemas.forecast_test_result import ForecastTestResult

def save_forecast_test_result_to_excel(result: ForecastTestResult) -> str:
    # Path to the project folder (tester/)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    results_dir = os.path.join(base_dir, "forecast_test_results")
    os.makedirs(results_dir, exist_ok=True)

    # Generate file name
    file_name = f"forecast_test_result_{datetime.now():%Y%m%d_%H%M%S}.xlsx"
    file_path = os.path.join(results_dir, file_name)

    data_dict = result.to_dict()

    # Creating an Excel file
    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        for sheet_name, data in data_dict.items():
            if data:
                df = pd.DataFrame(data)
                df.to_excel(writer, sheet_name=sheet_name[:31], index=False)
            else:
                pd.DataFrame([{"info": "No data"}]).to_excel(writer, sheet_name=sheet_name[:31], index=False)

    return file_path
