from fastapi import APIRouter

from api_v1.endpoints import login, dbt

api_router = APIRouter()
api_router.include_router(dbt.router, prefix="/dbt", tags=["dbt"])
api_router.include_router(login.router, tags=["login"])