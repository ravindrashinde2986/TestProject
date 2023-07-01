from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: str
    DATABASE_HOST_NAME: str
    DATABASE_NAME: str
    ALGORITHM: str
    SECRET: str
    EXPIRATION_TIME: int

    class Config:
        env_file = ".env"


settings = Settings()
