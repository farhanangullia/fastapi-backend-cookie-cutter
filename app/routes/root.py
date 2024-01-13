from fastapi import APIRouter
from pydantic import BaseModel
from starlette import status

router = APIRouter()


class HealthCheck(BaseModel):
    status: str = "OK"


@router.get(
    "/healthz",
    summary="Perform a Health Check",
    response_description="Return HTTP Status Code 200 (OK)",
    status_code=status.HTTP_200_OK,
    response_model=HealthCheck,
)
def get_health() -> HealthCheck:
    return HealthCheck(status="OK")
