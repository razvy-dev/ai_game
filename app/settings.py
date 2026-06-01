from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pydantic import SecretStr

class Settings(BaseSettings):
    """ App settings loaded from the .env file"""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    #postgres config

    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = ""
    postgres_user: str = ""
    postgres_password: str = ""

    # TODO: redis config

    redis_host: str = "localhost"
    redis_port: int = 6379

    # app stuff

    log_level: str = "DEBUG"

    # allowed origins

    frontend_origin: str = "http://lcalhost:3000"
    admin_origin: str = "http://localhost:5173"

    # authentication stuff

    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_expires_in_minutes: int = 30

    @property
    def postgres_dsn(self) -> str:
        """Build PostgreSQL connection string"""
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"

    @property
    def redis_url(self) -> str:
        """Build Redis connection string"""
        return f"redis://{self.redis_host}:{self.redis_port}/0"

    @property
    def allowed_origins(self) -> list[str]:
        """Build the allowed origins array"""
        return [self.admin_origin, self.frontend_origin]

@lru_cache
def get_settings() -> Settings:
    return Settings()

# Convenient global instance for configuration files
settings = get_settings()