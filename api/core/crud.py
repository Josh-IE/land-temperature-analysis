from typing import Optional

import sqlalchemy as sa
from sqlalchemy.orm import Session

from core import schemas
from core.models import Temperature


def create_temperature(db: Session, temperature_request: schemas.Temperature):
    temperature_record = Temperature(**temperature_request.dict())
    db.add(temperature_record)
    db.commit()
    db.refresh(temperature_record)
    return temperature_record


def update_temperature(
    db: Session, temperature_request: schemas.TemperatureUpdate, dt, city
):
    temperature_record = (
        db.query(Temperature)
        .filter(Temperature.dt == dt, Temperature.city == city)
        .first()
    )
    temperature_data = temperature_request.dict(exclude_unset=True)
    for key, value in temperature_data.items():
        setattr(temperature_record, key, value)
    db.add(temperature_record)
    db.commit()
    db.refresh(temperature_record)
    return temperature_record


def get_highest_temperature(db: Session, limit, start_date, end_date):
    records_within_dates = (
        db.query(Temperature)
        .filter(
            sa.and_(Temperature.dt <= end_date, Temperature.dt >= start_date)
        )
        .cte("temperature_records_within_date_range")
    )

    max_temperatures = (
        db.query(records_within_dates)
        .with_entities(
            records_within_dates.c.city,
            sa.func.max(records_within_dates.c.averagetemperature).label(
                "max_temperature"
            ),
        )
        .group_by(records_within_dates.c.city)
        .cte("max_temperatures")
    )

    city_max_temperatures = (
        db.query(max_temperatures)
        .order_by(
            sa.desc(max_temperatures.c.max_temperature),
            max_temperatures.c.city,
        )
        .limit(limit)
        .cte("city_max_temperatures")
    )

    return (
        db.query(Temperature)
        .join(
            city_max_temperatures,
            sa.and_(
                city_max_temperatures.c.max_temperature
                == Temperature.averagetemperature,
                city_max_temperatures.c.city == Temperature.city,
            ),
        )
        .order_by(
            sa.desc(city_max_temperatures.c.max_temperature),
            city_max_temperatures.c.city,
        )
    )
