from typing import List

from pydantic import BaseModel


class ForecastBody(BaseModel):
    forecast_type_id: int
    model_filter: List[int]
    forecast_segment_filter: int
    bayesian_optimization: bool


class ForecastInitialRequest(BaseModel):
    body: ForecastBody


class ParameterUpdate(BaseModel):
    forecast_segment_model_id: int
    parameter_id: int
    new_value: str


class ForecastTestRunRequest(BaseModel):
    body: ForecastBody
    item_ids: List[int]
    parameter_update_sets: List[List[ParameterUpdate]]
