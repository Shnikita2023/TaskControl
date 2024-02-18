from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class DbSettings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str

    DB_HOST_TEST: str
    DB_PORT_TEST: int
    DB_NAME_TEST: str
    DB_USER_TEST: str
    DB_PASS_TEST: str

    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_DB: str

    @property
    def database_url_asyncpg(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@" f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def database_test_url_asyncpg(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER_TEST}:{self.DB_PASS_TEST}@"
            f"{self.DB_HOST_TEST}:{self.DB_PORT_TEST}/{self.DB_NAME_TEST}"
        )

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


class Settings:
    db: DbSettings = DbSettings()


settings: Settings = Settings()
