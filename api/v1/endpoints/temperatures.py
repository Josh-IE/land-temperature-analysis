from datetime import date
from typing import List, Optional

from fastapi import Depends
from fastapi_pagination import Page, Params, paginate
from sqlalchemy.orm import Session

from core import schemas
from core.router import APIRouter
from usecases import (
    create_temperature_usecase,
    update_temperature_usecase,
    highest_temperature_usecase,
)
from core.database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", status_code=201, response_model=schemas.Temperature)
def create_temperature_entry(
    temperature_request: schemas.Temperature, db: Session = Depends(get_db)
):

    # Creates a new temperature record.
    create_temperature_usecase.db = db
    return create_temperature_usecase.execute(temperature_request)


@router.patch("/", response_model=schemas.Temperature)
def update_temperature_entry(
    temperature_request: schemas.TemperatureUpdate,
    dt: date,
    city: str,
    db: Session = Depends(get_db),
):
    # Updates a temperature record identified by its date and city.
    update_temperature_usecase.db = db
    return update_temperature_usecase.execute(temperature_request, dt, city)


@router.get("/highest", response_model=Page[schemas.Temperature])
def highest_temperature_cities(
    limit: int,
    start_date: date,
    end_date: Optional[date] = date.today(),
    params: Params = Depends(),
    db: Session = Depends(get_db),
):
    """
    Returns the top N cities that have the highest monthly AverageTemperature in
    a specified time range.
    """
    highest_temperature_usecase.db = db
    records = highest_temperature_usecase.execute(limit, start_date, end_date)
    return paginate(records, params)
