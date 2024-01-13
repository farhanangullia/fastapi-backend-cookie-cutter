from pydantic import BaseModel


class User(BaseModel):
    email: str


class Profile(BaseModel):
    email: str
