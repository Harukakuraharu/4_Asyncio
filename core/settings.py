from pydantic import computed_field
from pydantic_settings import BaseSettings


class Config(BaseSettings):

    POSTGRES_USER: str = "user"
    POSTGRES_PASSWORD: str = "user"
    POSTGRES_DB: str = "db"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432

    @computed_field
    def async_dsn(self) -> str:
        """Ссылка для асинхронного подключения к БД"""
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:"
            f"{self.POSTGRES_PASSWORD}@{self.DB_HOST}:"
            f"{self.DB_PORT}/{self.POSTGRES_DB}"
        )


config = Config()
