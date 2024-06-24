from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    templates_dir: str = "templates"

    database_url: str
    echo_queries: bool

    secret_key: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
