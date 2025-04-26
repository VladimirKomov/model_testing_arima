from typing import List, Dict, Any
from dataclasses import dataclass, asdict

@dataclass
class ForecastTestResult:
    forecast_overall: List[Dict[str, Any]]
    top_offenders: List[Dict[str, Any]]
    top_offenders_details: List[Dict[str, Any]]

    def to_dict(self) -> dict:
        return asdict(self)
