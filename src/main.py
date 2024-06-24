from fastapi import FastAPI

from src.index.router import router as index_router
from src.points_tables.router import router as points_tables_router
from src.auth.router import router as auth_router

from .database import Base, engine

Base.metadata.create_all(engine)

app = FastAPI()

app.include_router(index_router, prefix="/index")
app.include_router(points_tables_router, prefix="/tables")
app.include_router(auth_router, prefix="/auth")
