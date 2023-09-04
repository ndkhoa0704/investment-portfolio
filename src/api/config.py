from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str
    DATABASE_URI: str
    EXCLUDE_ENDPOINTS: list[str]


settings = Settings()