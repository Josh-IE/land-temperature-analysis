import logging

from core import crud, schemas

logger = logging.getLogger("uvicorn")


class CreateTemperatureUsecase:
    def __init__(self):
        self.db = None

    def execute(self, temperature_request):

        temperature_object = crud.create_temperature(
            self.db, temperature_request
        )

        return temperature_object


class UpdateTemperatureUsecase:
    def __init__(self):
        self.db = None

    def execute(self, temperature_request, dt, city):

        temperature_object = crud.update_temperature(
            self.db, temperature_request, dt, city
        )

        return temperature_object


class HighestTemperatureUsecase:
    def __init__(self):
        self.db = None

    def execute(self, limit, start_date, end_date):

        city_list = crud.get_highest_temperature(
            self.db, limit, start_date, end_date
        )

        return city_list.all()


create_temperature_usecase = CreateTemperatureUsecase()

update_temperature_usecase = UpdateTemperatureUsecase()

highest_temperature_usecase = HighestTemperatureUsecase()
