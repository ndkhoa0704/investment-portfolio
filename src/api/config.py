from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_API_KEY: str
    POSTGRES_URI: str
    class Config:
        env_file = 'prod.env'
        env_file_encoding = 'utf-8'


settings = Settings()