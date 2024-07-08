from fastapi import FastAPI

from src.auth.router import router as auth_router
from src.index.router import router as index_router
from src.points_tables.router import router as points_tables_router

app = FastAPI()

app.include_router(index_router, prefix="/index")
app.include_router(points_tables_router, prefix="/tables")
app.include_router(auth_router, prefix="/auth")
