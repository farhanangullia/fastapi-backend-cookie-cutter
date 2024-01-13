from fastapi import APIRouter, Request, Response, HTTPException
from pydantic import BaseModel
from starlette import status
from app.domain.services.user import UserService

router = APIRouter()


class ProfileResponse(BaseModel):
    email: str


# /user/info
# if not in table, populate table entry.
# returns roles/user object


@router.get(
    "/profile",
    summary="Retrieve own profile",
    status_code=status.HTTP_200_OK,
    response_model=ProfileResponse,
)
def get_profile(request: Request, response: Response):
    profile = UserService.get_profile(email="sampleuser@gmail.com")
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return ProfileResponse(email=profile.email)


@router.post(
    "/profile",
    summary="Update user last name",
    status_code=status.HTTP_200_OK,
    response_model=ProfileResponse,
)
def update_user_name(request: Request, response: Response):
    profile = UserService.update_user_last_name(email="sampleuser@gmail.com")
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return ProfileResponse(email=profile.email)
