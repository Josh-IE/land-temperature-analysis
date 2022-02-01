from sys import prefix
from fastapi import FastAPI

from v1 import api_router
from core.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(api_router, prefix="/v1")
