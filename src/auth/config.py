from src.config import Settings as GlobalSettings


class Settings(GlobalSettings):
    token_hash_alg: str = "HS256"
    token_expire_minutes: int = 60


settings = Settings()
