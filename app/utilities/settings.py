import os
from pydantic import Field
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
)

ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env", f".env.{ENVIRONMENT}"),
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = Field()
    DEBUG: bool = Field(default=True)
    LOG_LEVEL: str = Field(default="INFO")
    CORS_ORIGINS: list = Field()
    AWS_REGION: str = Field(default="ap-southeast-1")
    AWS_ENDPOINT: str = Field(default="")
    DYNAMODB_HOST: str = Field(default="")
    DUMMY_AWS_KEY: str = Field(default="")


settings = Settings()
