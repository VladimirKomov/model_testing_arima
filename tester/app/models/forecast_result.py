from sqlalchemy import Column, Integer, Text, String, Boolean, ForeignKey

from app.databases.postgresql import Base


class ForecastSegmentModelParameter(Base):
    __tablename__ = "forecast_segment_model_params"

    forecast_segment_model_id = Column(
        Integer,
        ForeignKey("forecast_segment_models.id"),
        primary_key=True
    )
    parameter_id = Column(
        Integer,
        ForeignKey("forecast_parameters.id"),
        primary_key=True
    )
    value = Column(Text, nullable=False)

    use_bayesian_optimization = Column(Boolean, nullable=True)
    feature_as_columns = Column(Boolean, nullable=True)
    value_options = Column(String(100), nullable=True)
