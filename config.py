from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    DB_USERNAME: str
    DB_PASSWORD: str


settings = Settings()
