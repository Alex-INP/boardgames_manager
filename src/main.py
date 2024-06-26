from fastapi import FastAPI
import pika

from src.index.router import router as index_router
from src.points_tables.router import router as points_tables_router
from src.auth.router import router as auth_router


app = FastAPI()

app.include_router(index_router, prefix="/index")
app.include_router(points_tables_router, prefix="/tables")
app.include_router(auth_router, prefix="/auth")

def setup_rabbit_mq_channels():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    try:
        channel = connection.channel()
    except Exception:
        connection.close()
    channel.queue_declare(queue="tasks")
    connection.close()

setup_rabbit_mq_channels()