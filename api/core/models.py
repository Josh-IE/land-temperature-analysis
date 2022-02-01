from sqlalchemy import Column, Float, String, Date

from core.database import Base


class Temperature(Base):
    __tablename__ = "Global_Land_Temperatures_By_City"

    dt = Column(Date, primary_key=True)
    averagetemperature = Column(Float)
    averagetemperatureuncertainty = Column(Float)
    city = Column(String, primary_key=True)
    country = Column(String)
    latitude = Column(String)
    longitude = Column(String)
