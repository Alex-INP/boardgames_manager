from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str
    echo_queries: bool
    session_action_on_factory_obj_created: str = "flush"

    model_config = SettingsConfigDict(env_file=".env.tests")


settings = Settings()
