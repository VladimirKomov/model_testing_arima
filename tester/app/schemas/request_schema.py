from pydantic import BaseModel
from typing import List

class ForecastBody(BaseModel):
    forecast_type_id: int
    model_filter: List[int]
    forecast_segment_filter: int
    bayesian_optimization: bool

class ForecastRequest(BaseModel):
    body: ForecastBody
