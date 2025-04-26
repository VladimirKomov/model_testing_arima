from sqlalchemy import Integer, JSON, Column

from app.databases.postgresql import Base


class ForecastResult(Base):
    __tablename__ = "forecast_results"

    id = Column(Integer, primary_key=True, index=True)
    result = Column(JSON)
