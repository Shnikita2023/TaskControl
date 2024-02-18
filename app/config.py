from pydantic_settings import BaseSettings, SettingsConfigDict


class DbSettings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5460
    DB_NAME: str = "task_db"
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"

    DB_HOST_TEST: str = "localhost"
    DB_PORT_TEST: int = 5461
    DB_NAME_TEST: str = "task_db_test"
    DB_USER_TEST: str = "postgres"
    DB_PASS_TEST: str = "postgres"

    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_USER: str = "postgres"
    POSTGRES_DB: str = "task_db"

    @property
    def database_url_asyncpg(self) -> str:
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )

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
