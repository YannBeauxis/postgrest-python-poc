from pydantic import BaseSettings


class Settings(BaseSettings):
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    role: str = "admin"

    class Config:
        env_prefix = "auth_api_"


settings = Settings()  # type: ignore
