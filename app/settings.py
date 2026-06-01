from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """ App settings loaded from the .env file"""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False
    )

    #postgres config

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = ""
    postgres_user: str = ""
    postgres_password: str = ""

    # TODO: redis config

    # app stuff

    log_level: str = "DEBUG"

    @property
    def postgres_dsn(self) -> str:
        """Build PostgreSQL connection string"""
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @property
    def redis_url(self) -> str:
        """Build Redis connection string"""
        return f"redis://{self.redis_host}:{self.redis_port}/0"