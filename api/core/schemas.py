from datetime import date
from typing import Optional

from pydantic import BaseModel, validator


class Temperature(BaseModel):
    dt: date
    averagetemperature: Optional[float]
    averagetemperatureuncertainty: Optional[float]
    city: str
    country: str
    latitude: str
    longitude: str

    class Config:
        orm_mode = True


class TemperatureUpdate(BaseModel):
    averagetemperature: Optional[float]
    averagetemperatureuncertainty: Optional[float]

    @validator("averagetemperatureuncertainty")
    def temperature_provided(cls, v, values, **kwargs):
        if not v and not values["averagetemperature"]:
            raise ValueError(
                "averagetemperature or averagetemperatureuncertainty is required"
            )
        if v and values["averagetemperature"]:
            raise ValueError(
                "averagetemperature and averagetemperatureuncertainty cannot be provided together"
            )
        return v
