from pathlib import PurePath

from pydantic_settings import BaseSettings

from src.config import settings as global_settings


class Settings(BaseSettings):
    index_templates_dir: str = str(PurePath(global_settings.templates_dir, "index"))


settings = Settings()
