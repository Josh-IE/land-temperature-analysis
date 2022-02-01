from fastapi import APIRouter

from v1.endpoints import temperatures


api_router = APIRouter()
api_router.include_router(
    temperatures.router, prefix="/temperatures", tags=["temperatures"]
)
