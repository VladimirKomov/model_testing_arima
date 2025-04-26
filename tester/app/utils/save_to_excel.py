import pandas as pd
from app.schemas.forecast_test_result import ForecastTestResult
import os

def save_forecast_test_result_to_excel(result: ForecastTestResult, file_path: str):
    data_dict = result.to_dict()

    # Создаём Excel-файл
    with pd.ExcelWriter(file_path, engine="openpyxl") as writer:
        for sheet_name, data in data_dict.items():
            if data:  # Проверяем, что не пустой список
                df = pd.DataFrame(data)
                df.to_excel(writer, sheet_name=sheet_name[:31], index=False)  # Ограничение Excel: имя sheet <= 31 символ
            else:
                # Если данных нет, создаём пустую страницу
                pd.DataFrame([{"info": "No data"}]).to_excel(writer, sheet_name=sheet_name[:31], index=False)
