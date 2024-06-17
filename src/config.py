from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    templates_dir: str = "templates"
    db_name: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
