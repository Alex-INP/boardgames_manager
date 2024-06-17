from fastapi import FastAPI

from src.index.router import router as index_router
from src.config import settings

app = FastAPI()

app.include_router(index_router, prefix="/index")

